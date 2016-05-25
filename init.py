# encoding: utf-8

import sys
import shell
from workflow import Workflow, ICON_ERROR

shells = ["fish", "bash"]

def getVariables(shellName):

	def fish():
		variables = sh.execute(["/usr/local/bin/fish", "-c", "set"])
		variables = variables.split("\n")
		result = []
		for variable in variables:
			if len(variable):
				tmp = variable.split(" ")
				result.append({"name": unicode(tmp[0].decode("utf-8")), "value": unicode(" ".join(tmp[1:]).decode("utf-8"))})
		return result

	def bash():
		variables = sh.execute(["/bin/bash", "-ic", "export"])
		variables = variables.split("\n")
		result = []
		for variable in variables:
			if len(variable):
				variable = variable.replace("declare -x", "")
				tmp = variable.split("=")
				result.append({"name": unicode(tmp[0].decode("utf-8")), "value": unicode("=".join(tmp[1:]).decode("utf-8"))})
		return result

	sh = shell.Shell()
	if shellName in shells:
		return locals()[shellName]()

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
