"""Translate human-readable Jovial labels into HP-16C program labels.

The HP-16C has only 16 physical program labels: ``0`` through ``9`` and
``A`` through ``F``. Jovial source can instead use case-insensitive symbolic
names, for example::

    retry:
        GTO retry

This module performs the extra pass needed to translate that source into the
calculator instructions ``LBL 0`` and ``GTO 0`` before the ordinary Jovial
instruction parser sees it.

Supported declarations
----------------------
``name:``
    Declare an automatically allocated symbolic label. This is the preferred
    syntax for new Jovial programs.
``LBL name``
    Equivalent calculator-style spelling of ``name:``.
``LBL name = A``
    Declare a symbol but pin it to a particular physical label. Pinning is
    needed when a program computes a label at run time with ``GTO I``, or when
    preserving the exact keystrokes of an existing calculator program.
``LBL A``
    Legacy physical-label syntax. It is passed through unchanged.

Resolution deliberately happens in two logical passes. The first pass finds
all definitions and reserves every physical label mentioned anywhere in the
file. It then assigns the remaining physical labels to automatic symbols in
declaration order. The second pass rewrites declarations and symbolic
``GTO``/``GSB`` references. This is why a branch can refer to a symbol that is
declared later in the file.
"""

import re


# Automatic labels are allocated in this order after explicitly used labels
# have been removed. These are the only label keys available on the HP-16C.
PHYSICAL_LABELS = tuple("0123456789ABCDEF")

# These operands are not symbols. They tell GTO/GSB to obtain the destination
# indirectly from the calculator's I register, so they must pass through.
INDIRECT_LABELS = {"i", "(i)"}

# Symbol names intentionally resemble identifiers in conventional assembly
# languages. Dashes and punctuation are rejected so tokenization is clear.
SYMBOL_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class LabelResolutionError(ValueError):
    """Raised when symbolic labels cannot be mapped to HP-16C labels."""


def resolve_symbolic_labels(assembly_code):
    """Resolve symbolic labels and return calculator-ready assembly source.

    Symbolic labels are case-insensitive and may be declared as either
    ``name:`` or ``LBL name``. The optional ``LBL name = A`` form pins a
    symbol to a physical HP-16C label, which is useful when preserving an
    existing program's exact keystrokes.

    Args:
        assembly_code: An iterable of source lines. Lines normally include
            their trailing newline because they come from ``readlines()``.

    Returns:
        A two-item tuple containing:

        * The rewritten source lines accepted by the existing instruction
          parser. Symbolic declarations become physical ``LBL`` instructions,
          and symbolic branches become physical ``GTO``/``GSB`` instructions.
        * A dictionary mapping each lower-case symbolic name to its assigned
          one-character physical label.

    Raises:
        LabelResolutionError: If a declaration is malformed, a symbol is
            invalid/duplicated/undefined, or more automatic symbols are used
            than the calculator has available physical labels.
    """
    # Parse comments and tokens just once. Keeping the original line alongside
    # the parsed form lets unchanged instructions retain their exact spelling,
    # indentation, comments, and line endings.
    parsed_lines = [_parse_source_line(line, line_number)
                    for line_number, line in enumerate(assembly_code, start=1)]

    # PASS 1A: discover declarations and reserve explicitly mentioned labels.
    #
    # Reservation is global rather than dependent on source order. For
    # example, an automatic symbol near the top must not take label A if a
    # legacy `GTO A` appears near the bottom. Pinned labels are reserved for
    # the same reason.
    reserved_labels = set()
    definitions = []

    for source_line in parsed_lines:
        tokens = source_line["tokens"]
        if not tokens:
            continue

        instruction = tokens[0].lower()
        if instruction in {"lbl", "gto", "gsb"} and len(tokens) == 2:
            target = tokens[1]
            if _is_physical_label(target):
                reserved_labels.add(target.upper())

        # A definition is represented as (symbol, pinned physical label). The
        # pinned value is None for an automatically allocated declaration.
        definition = _get_definition(source_line)
        if definition is not None:
            symbol, pinned_label = definition
            definitions.append((symbol, pinned_label, source_line["line_number"]))
            if pinned_label is not None:
                reserved_labels.add(pinned_label)

    # PASS 1B: allocate the symbol table. Symbols are normalized to lower case
    # so declarations and references are case-insensitive. Physical labels are
    # always stored in their canonical upper-case form.
    symbol_table = {}
    available_labels = [label for label in PHYSICAL_LABELS
                        if label not in reserved_labels]

    for symbol, pinned_label, line_number in definitions:
        normalized_symbol = symbol.lower()
        if normalized_symbol in symbol_table:
            raise LabelResolutionError(
                f"Duplicate symbolic label '{symbol}' on line {line_number}."
            )

        if pinned_label is not None:
            # Different symbolic names may intentionally share one pinned
            # physical label. The HP-16C searches forward for labels, and the
            # Towers of Hanoi sample relies on two occurrences of LBL 1.
            symbol_table[normalized_symbol] = pinned_label
        elif available_labels:
            # pop(0) makes allocation deterministic: 0-9, then A-F, excluding
            # every physical label reserved above.
            symbol_table[normalized_symbol] = available_labels.pop(0)
        else:
            raise LabelResolutionError(
                f"Cannot allocate symbolic label '{symbol}' on line {line_number}: "
                "the HP-16C has only 16 program labels (0-9 and A-F)."
            )

    # PASS 2: produce source understood by Parse_File.parse_line(). That parser
    # deliberately remains unaware of symbolic labels; it receives only the
    # physical operands the HP-16C can encode.
    resolved_code = []
    for source_line in parsed_lines:
        tokens = source_line["tokens"]
        if not tokens:
            # Blank and comment-only lines never need rewriting.
            resolved_code.append(source_line["original"])
            continue

        definition = _get_definition(source_line)
        if definition is not None:
            symbol, _ = definition
            # A source declaration such as `loop:` becomes `lbl 0`. Preserve
            # any comment following the declaration for useful debug logging.
            resolved_code.append(
                _with_comment(f"lbl {symbol_table[symbol.lower()]}", source_line)
            )
            continue

        instruction = tokens[0].lower()
        if instruction in {"gto", "gsb"} and len(tokens) == 2:
            target = tokens[1]
            # Physical and indirect operands are already calculator-ready.
            # Every other operand in this position is required to be a valid,
            # declared symbolic name.
            if not _is_physical_label(target) and target.lower() not in INDIRECT_LABELS:
                _validate_symbol(target, source_line["line_number"])
                normalized_target = target.lower()
                if normalized_target not in symbol_table:
                    raise LabelResolutionError(
                        f"Undefined symbolic label '{target}' on line "
                        f"{source_line['line_number']}."
                    )
                resolved_code.append(
                    _with_comment(
                        f"{instruction} {symbol_table[normalized_target]}", source_line
                    )
                )
                continue

        # Ordinary calculator instructions and legacy label instructions pass
        # through byte-for-byte.
        resolved_code.append(source_line["original"])

    return resolved_code, symbol_table


def _parse_source_line(line, line_number):
    """Return the representations needed by both resolution passes.

    ``code`` excludes comments and surrounding whitespace. ``tokens`` are
    split only on whitespace because Jovial's label forms do not need a more
    complicated lexer. ``original`` is retained for unchanged output.
    """
    code, comment = _split_comment(line.rstrip("\n"))
    return {
        "original": line,
        "code": code.strip(),
        "comment": comment,
        "tokens": code.strip().split(),
        "line_number": line_number,
    }


def _split_comment(line):
    """Split a line at its earliest Jovial comment marker.

    Jovial accepts both ``//`` and ``;``. Taking the earliest occurrence
    matches the behavior of the main parser when a line contains both forms.
    The returned comment includes its marker so rewritten lines can preserve
    it.
    """
    comment_indexes = [index for marker in ("//", ";")
                       if (index := line.find(marker)) != -1]
    if not comment_indexes:
        return line, ""

    comment_index = min(comment_indexes)
    return line[:comment_index], line[comment_index:]


def _with_comment(code, source_line):
    """Attach a preserved source comment to one rewritten code line."""
    comment = source_line["comment"]
    return f"{code} {comment}\n" if comment else f"{code}\n"


def _get_definition(source_line):
    """Parse a symbolic declaration, or return ``None`` for other lines.

    The return value is ``(symbol, pinned_label)``. ``pinned_label`` is None
    for ``name:`` and ``LBL name`` declarations. Legacy ``LBL 0``-``LBL F``
    and indirect spellings are not symbolic definitions, so they return None
    and are left for the existing instruction parser.
    """
    code = source_line["code"]
    tokens = source_line["tokens"]
    line_number = source_line["line_number"]

    if code.endswith(":"):
        # Traditional form. A label must occupy its own source line; Jovial
        # does not currently support `loop: instruction` on one line.
        symbol = code[:-1].strip()
        if not symbol or len(symbol.split()) != 1:
            raise LabelResolutionError(
                f"Invalid symbolic label declaration on line {line_number}."
            )
        _validate_symbol(symbol, line_number)
        return symbol, None

    if not tokens or tokens[0].lower() != "lbl":
        return None

    if len(tokens) == 2:
        target = tokens[1]
        # Preserve the original calculator syntax. In particular, `LBL A`
        # means physical label A rather than a one-letter symbol named "A".
        if _is_physical_label(target) or target.lower() in INDIRECT_LABELS:
            return None
        _validate_symbol(target, line_number)
        return target, None

    if len(tokens) == 4 and tokens[2] == "=":
        # Pinned form: LBL descriptive_name = physical_label
        symbol = tokens[1]
        physical_label = tokens[3]
        _validate_symbol(symbol, line_number)
        if not _is_physical_label(physical_label):
            raise LabelResolutionError(
                f"Invalid physical label '{physical_label}' on line {line_number}; "
                "expected 0-9 or A-F."
            )
        return symbol, physical_label.upper()

    raise LabelResolutionError(
        f"Invalid LBL declaration on line {line_number}. Use 'LBL A', "
        "'LBL name', 'name:', or 'LBL name = A'."
    )


def _validate_symbol(symbol, line_number):
    """Validate one symbolic name and report its source line on failure."""
    if not SYMBOL_PATTERN.fullmatch(symbol):
        raise LabelResolutionError(
            f"Invalid symbolic label '{symbol}' on line {line_number}. Labels must "
            "start with a letter or underscore and contain only letters, digits, "
            "and underscores."
        )
    if _is_physical_label(symbol) or symbol.lower() in INDIRECT_LABELS:
        # Reject names whose meaning would be ambiguous with a real calculator
        # operand. Longer names such as `a_loop` and `index` remain valid.
        raise LabelResolutionError(
            f"'{symbol}' is reserved by the HP-16C and cannot be a symbolic label "
            f"(line {line_number})."
        )


def _is_physical_label(label):
    """Return whether ``label`` is exactly one HP-16C label key (0-9/A-F)."""
    return len(label) == 1 and label.upper() in PHYSICAL_LABELS
