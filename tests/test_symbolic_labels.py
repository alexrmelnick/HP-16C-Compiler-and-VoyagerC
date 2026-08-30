"""Focused tests for the symbolic HP-16C label resolver."""

import sys
import unittest
from pathlib import Path


SOURCE_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_DIRECTORY))

from Symbolic_Labels import LabelResolutionError, resolve_symbolic_labels


class SymbolicLabelResolutionTests(unittest.TestCase):
    def test_colon_declaration_is_allocated_and_comments_are_preserved(self):
        resolved, symbols = resolve_symbolic_labels(
            ["start: // program entry\n", "GTO start ; repeat\n"]
        )

        self.assertEqual(
            resolved,
            ["lbl 0 // program entry\n", "gto 0 ; repeat\n"],
        )
        self.assertEqual(symbols, {"start": "0"})

    def test_lbl_declaration_supports_forward_gto_and_gsb_references(self):
        resolved, symbols = resolve_symbolic_labels(
            [
                "GTO Finished\n",
                "GSB HELPER\n",
                "LBL helper\n",
                "finished:\n",
            ]
        )

        self.assertEqual(
            resolved,
            ["gto 1\n", "gsb 0\n", "lbl 0\n", "lbl 1\n"],
        )
        self.assertEqual(symbols, {"helper": "0", "finished": "1"})

    def test_symbols_are_case_insensitive(self):
        resolved, symbols = resolve_symbolic_labels(
            ["Loop_Start:\n", "gto LOOP_START\n", "gsb loop_start\n"]
        )

        self.assertEqual(resolved, ["lbl 0\n", "gto 0\n", "gsb 0\n"])
        self.assertEqual(symbols, {"loop_start": "0"})

    def test_legacy_physical_and_indirect_labels_are_unchanged(self):
        source = [
            "LBL 0\n",
            "lbl a ; lowercase physical label\n",
            "GTO F\n",
            "gsb b\n",
            "GTO I\n",
            "GSB (i)\n",
        ]

        resolved, symbols = resolve_symbolic_labels(source)

        self.assertEqual(resolved, source)
        self.assertEqual(symbols, {})

    def test_physical_and_pinned_labels_are_reserved_before_allocation(self):
        resolved, symbols = resolve_symbolic_labels(
            [
                "LBL F\n",
                "GTO 0\n",
                "GSB A\n",
                "first:\n",
                "LBL fixed = 2\n",
                "second:\n",
                "GTO first\n",
                "GTO fixed\n",
                "GTO second\n",
            ]
        )

        self.assertEqual(
            resolved,
            [
                "LBL F\n",
                "GTO 0\n",
                "GSB A\n",
                "lbl 1\n",
                "lbl 2\n",
                "lbl 3\n",
                "gto 1\n",
                "gto 2\n",
                "gto 3\n",
            ],
        )
        self.assertEqual(symbols, {"first": "1", "fixed": "2", "second": "3"})

    def test_pinned_label_is_normalized_and_can_be_referenced(self):
        resolved, symbols = resolve_symbolic_labels(
            ["LBL worker = e ; chosen entry\n", "GSB Worker\n"]
        )

        self.assertEqual(
            resolved,
            ["lbl E ; chosen entry\n", "gsb E\n"],
        )
        self.assertEqual(symbols, {"worker": "E"})

    def test_distinct_symbols_may_share_a_pinned_physical_label(self):
        resolved, symbols = resolve_symbolic_labels(
            [
                "LBL forward = A\n",
                "LBL reverse = a\n",
                "GTO forward\n",
                "GTO reverse\n",
            ]
        )

        self.assertEqual(
            resolved,
            ["lbl A\n", "lbl A\n", "gto A\n", "gto A\n"],
        )
        self.assertEqual(symbols, {"forward": "A", "reverse": "A"})

    def test_undefined_reference_is_rejected(self):
        with self.assertRaisesRegex(
            LabelResolutionError,
            r"Undefined symbolic label 'missing' on line 2",
        ):
            resolve_symbolic_labels(["HEX\n", "GTO missing\n"])

    def test_duplicate_symbol_is_rejected_case_insensitively(self):
        with self.assertRaisesRegex(
            LabelResolutionError,
            r"Duplicate symbolic label 'LOOP' on line 2",
        ):
            resolve_symbolic_labels(["loop:\n", "LBL LOOP\n"])

    def test_invalid_symbol_names_are_rejected_in_declarations_and_references(self):
        invalid_sources = {
            "colon declaration": (["bad-name:\n"], r"Invalid symbolic label 'bad-name'"),
            "LBL declaration": (["LBL 2bad\n"], r"Invalid symbolic label '2bad'"),
            "reference": (["GTO bad-name\n"], r"Invalid symbolic label 'bad-name'"),
            "reserved name": (["i:\n"], r"'i' is reserved by the HP-16C"),
        }

        for description, (source, message) in invalid_sources.items():
            with self.subTest(description=description):
                with self.assertRaisesRegex(LabelResolutionError, message):
                    resolve_symbolic_labels(source)

    def test_invalid_lbl_forms_and_pin_targets_are_rejected(self):
        invalid_sources = {
            "missing symbol": (["LBL\n"], r"Invalid LBL declaration on line 1"),
            "extra token": (["LBL name extra\n"], r"Invalid LBL declaration on line 1"),
            "invalid pin": (["LBL name = 10\n"], r"Invalid physical label '10'"),
            "invalid colon form": (["not a label:\n"], r"Invalid symbolic label declaration"),
        }

        for description, (source, message) in invalid_sources.items():
            with self.subTest(description=description):
                with self.assertRaisesRegex(LabelResolutionError, message):
                    resolve_symbolic_labels(source)

    def test_all_sixteen_physical_labels_can_be_allocated(self):
        source = [f"label_{index}:\n" for index in range(16)]

        resolved, symbols = resolve_symbolic_labels(source)

        expected_labels = list("0123456789ABCDEF")
        self.assertEqual(resolved, [f"lbl {label}\n" for label in expected_labels])
        self.assertEqual(
            symbols,
            {f"label_{index}": label for index, label in enumerate(expected_labels)},
        )

    def test_seventeenth_unpinned_symbol_exhausts_label_space(self):
        source = [f"label_{index}:\n" for index in range(17)]

        with self.assertRaisesRegex(
            LabelResolutionError,
            r"Cannot allocate symbolic label 'label_16' on line 17.*only 16",
        ):
            resolve_symbolic_labels(source)


if __name__ == "__main__":
    unittest.main()
