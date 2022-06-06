
# Infrastructure for the "Taxes" problem at DiceCTF 2022

How it works:

1. Programs are written as a dataflow graph with z3 (any graph format will work but I'm already familiar with z3). (see `part1.py`, `part2.py`, ...)
2. `flatten_ast` converts the z3 AST to a sequential list of operations and also caches constants so they only appear once
3. `ops_to_lines` converts the operation list to a JSON file with formatted text
4. `/builder` runs a simple webserver that uses Handlebars templating to convert the JSON files into nicely formatted HTML
5. (external) "Print" the HTML pages and save as PDF to render
