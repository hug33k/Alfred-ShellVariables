# encoding: utf-8

import sys
import shell
from workflow import Workflow, ICON_ERROR

shells = {
	"fish": {
		"cmd": ["/usr/local/bin/fish", "-c", "set"],
		"replace": {},
		"separator": " "
	},
	"bash": {
		"cmd": ["/bin/bash", "-ic", "export"],
		"replace": {"declare -x": ""},
		"separator": "="
	},
	"zsh": {
		"cmd": ["/bin/zsh", "-ic", "export"],
		"replace": {},
		"separator": "="
	},
}

def getVariables(shellName):

	def _getVars(cmd):
		variables = sh.execute(cmd)
		return variables.split(b"\n")

	def _split(item, symbol):
		tmp = item.split(symbol)
		return {"name": unicode(tmp[0].decode("utf-8")), "value": unicode(symbol.join(tmp[1:]).decode("utf-8"))}

	def execute(shellInfos):
		variables = _getVars(shellInfos["cmd"])
		result = []
		for variable in variables:
			if len(variable):
				for pattern in shellInfos["replace"]:
					variable = variable.replace(pattern, shellInfos["replace"][pattern])
				result.append(_split(variable, shellInfos["separator"]))
		return result

	sh = shell.Shell()
	if shellName in shells:
		return execute(shells[shellName])
	return None

def main(wf):
	try:
		wf.settings["data"] = getVariables(wf.settings["shell"])
	except:
		wf.add_item(title="Missing shell",
					subtitle="You should run sv shell",
					icon=ICON_ERROR)
	wf.send_feedback()

if __name__ == "__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
