"""examples/basic_usage.py — Basic library usage"""
from csprotocol import parse_command, generate_one_liner, handle

cmd = parse_command('g "Add CLI support"')
print(cmd)
# Command(base='g', argument='Add CLI support', flags=set())

print(generate_one_liner(cmd))
# python3 -c "import updater; updater.run(...)"

print(handle("g dry"))
print(handle("m force"))
print(handle("go"))        # ERROR: syntax: unknown command 'go'
