import sys
from pathlib import Path
from string import Template as Tp
from Generator import Generator, gen_token_enum, gen_token_name
from DATA import TERMINALS
LICENSE_TPL = """/**
 * License
 *
 * ${projectDescription}
 * Copyright (C) 2024 Yaokai Liu
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * Project Name: ${projectName}
 * Module Name: ${moduleName}
 * Filename: ${filename}
 * Copyright (c) 2024 Yaokai Liu. All rights reserved.
 **/
"""
if __name__ == '__main__':
    JSON_DIR = Path(sys.argv[1])
    TEMPLATE_DIR = Path(sys.argv[2])
    OUT_DIR = Path(sys.argv[3])

    myLicense = Tp(LICENSE_TPL).substitute(
        projectDescription="x-regex - A light regular expression and its compiler",
        projectName="regex",
        moduleName="grammar",
        filename="${filename}",
    )

    GRegex = Generator(json_dir=JSON_DIR / "regex",
                       template_dir=TEMPLATE_DIR / "regex",
                       out_dir=OUT_DIR / "regex",
                       target="Regex")
    GRegex.set_license(Tp(myLicense).substitute(filename="${filename}"))
    tokens = sorted(set(GRegex.tokens) | set(TERMINALS.keys()))
    GRegex.set_extend_tokens(tokens)

    myLicense = Tp(myLicense).substitute(filename="${filename}")

    gen_token_enum(TEMPLATE_DIR / "tokens.h.tpl",
                   Tp(myLicense).substitute(filename="tokens.gen.h"),
                   "Regex",
                   tokens,
                   OUT_DIR / "tokens.gen.h")

    gen_token_name(TEMPLATE_DIR / "tokens.c.tpl",
                   Tp(myLicense).substitute(filename="tokens.gen.c"),
                   "Regex",
                   tokens,
                   OUT_DIR / "tokens.gen.c")

    GRegex.set_context("RegexContext")
    GRegex.set_token_prefix("Regex")
    GRegex.set_prefix("Regex")
    GRegex.generate()
