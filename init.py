# encoding: utf-8

import sys
import shell
from workflow import Workflow

def getVariables():
	sh = shell.Shell()
	variables = sh.execute(["/usr/local/bin/fish", "-c", "set"])
	variables = variables.split("\n")
	result = []
	for variable in variables:
		if len(variable):
			tmp = variable.split(" ")
			result.append({"name": unicode(tmp[0].decode("utf-8")), "value": unicode(" ".join(tmp[1:]).decode("utf-8"))})
	return result

def main(wf):
	wf.settings["data"] = getVariables()
	wf.send_feedback()

if __name__ == "__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
