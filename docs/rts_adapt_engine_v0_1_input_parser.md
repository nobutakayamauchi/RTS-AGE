# RTS Adapt Engine v0.1 Input Reader and Section Parser

## Purpose

This PR adds the first local input parsing layer for RTS Adapt Engine v0.1.

It reads `inputs/daily_input.md` and parses Markdown heading sections into a structured object.

This is not an output generation PR.

---

## Added Modules

```text
src/input_reader.py
src/section_parser.py
```

---

## Supported Sections

```text
今日の現状
今日やったこと
詰まっていること
次にやること
使いたいネタ
参考URL
言いたいこと
言ってはいけないこと
出力したい媒体
今日の温度感
売りたい商品・サービス
誘導したい行動
LINE公式でやりたいこと
無料配布物
相談導線
注意事項
```

---

## Parser Behavior

The parser should:

```text
read local UTF-8 Markdown
parse supported headings
preserve unsupported headings separately
tolerate missing supported sections
preserve preamble text before the first heading
```

The parser should not:

```text
generate outputs
call model APIs
call external APIs
execute connectors
publish content
send messages
read credentials
write credentials
```

---

## CLI Behavior

The scaffold command now reads and parses the input file:

```bash
python src/generate.py
```

Expected status output includes:

```text
RTS Adapt Engine v0.1 input parser ready.
present_sections=<count>
missing_sections=<count>
unknown_sections=<count>
generation_not_implemented=true
external_api_calls=false
publishing=false
```

---

## Tests

The tests cover:

```text
supported section extraction
missing section tolerance
unknown section preservation
preamble preservation
scaffold command status output
```

---

## Next Implementation Step

After this parser PR is reviewed and merged, the next PR should be:

```text
PR-03: Add context normalizer
```

That next PR should transform parsed input into `outputs/context_summary.md` and should still avoid platform-specific draft generation.
