"""Regression tests for the checked-in Jovial sample programs."""

import re
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = REPOSITORY_ROOT / "src"
SAMPLE_DIRECTORY = REPOSITORY_ROOT / "tests" / "Jovial Assembler (.jov)"
JRPN_DIRECTORY = REPOSITORY_ROOT / "tests" / "JRPN Simulator (.16c)"
EMULATOR_DIRECTORY = REPOSITORY_ROOT / "tests" / "HP16C Emulator (.txt)"
sys.path.insert(0, str(SOURCE_DIRECTORY))

from Calculator_State import CalculatorState
from Parse_File import parse_line
from Symbolic_Labels import resolve_symbolic_labels


def assembled_key_positions(source_path):
    state = CalculatorState()
    state.update_base(10)
    source, _ = resolve_symbolic_labels(source_path.read_text().splitlines(keepends=True))

    for line_number, line in enumerate(source, start=1):
        parse_line(line, line_number, state)

    signature = []
    for instruction in state.program:
        keys = []
        if instruction.has_modifier:
            keys.append(str(instruction.modifier_position).strip())
        keys.append(str(instruction.instruction_position).strip())
        if instruction.has_argument:
            keys.append(str(instruction.argument_position).strip())
        signature.append(keys)

    return signature


def committed_jrpn_key_positions(output_path):
    signature = []
    for line in output_path.read_text().splitlines():
        match = re.match(r"\s+(\d{3})\s+\{\s*([^}]*)\}", line)
        if match is None or match.group(1) == "000":
            continue
        signature.append(match.group(2).split())
    return signature


def committed_emulator_key_positions(output_path):
    signature = []
    for line in output_path.read_text().splitlines():
        match = re.match(r"\s+(\d{3})\s+-\s+(.*?)\s*\|", line)
        if match is None or match.group(1) == "000":
            continue
        signature.append(match.group(2).replace(",", " ").split())
    return signature


class SampleProgramRegressionTests(unittest.TestCase):
    def test_samples_use_automatic_labels_except_towers_dispatch(self):
        pinned_labels = []
        for sample in sorted(SAMPLE_DIRECTORY.glob("*.jov")):
            for line in sample.read_text().splitlines():
                if re.match(r"(?i)^\s*lbl\s+\w+\s*=", line):
                    pinned_labels.append((sample.name, line.strip()))

        self.assertEqual(
            pinned_labels,
            [
                ("towers-of-hanoi.jov", "lbl dispatch_move = 1"),
                ("towers-of-hanoi.jov", "lbl special_move = 0"),
                ("towers-of-hanoi.jov", "lbl advance_disk = 1"),
            ],
        )

    def test_samples_match_committed_output_key_sequences(self):
        jrpn_outputs = {
            output.stem.lower(): output for output in JRPN_DIRECTORY.glob("*.16c")
        }
        emulator_outputs = {
            output.stem.lower(): output for output in EMULATOR_DIRECTORY.glob("*.txt")
        }
        samples = sorted(SAMPLE_DIRECTORY.glob("*.jov"))

        self.assertEqual(len(samples), 14)
        instruction_count = 0
        for sample in samples:
            with self.subTest(sample=sample.name):
                self.assertIn(sample.stem.lower(), jrpn_outputs)
                self.assertIn(sample.stem.lower(), emulator_outputs)
                assembled = assembled_key_positions(sample)
                self.assertEqual(
                    assembled,
                    committed_jrpn_key_positions(jrpn_outputs[sample.stem.lower()]),
                )
                self.assertEqual(
                    assembled,
                    committed_emulator_key_positions(
                        emulator_outputs[sample.stem.lower()]
                    ),
                )
                instruction_count += len(assembled)

        self.assertEqual(instruction_count, 653)


if __name__ == "__main__":
    unittest.main()
