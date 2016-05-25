# encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB, ICON_ERROR, ICON_INFO
from workflow.background import run_in_background, is_running

def filterVariables(variable):
	elements = []
	elements.append(variable["name"])
	elements.append(variable["value"])
	return u' '.join(elements)

def main(wf):
	if len(wf.args) and "-u" in wf.args:
		cmd = ['/usr/bin/python', wf.workflowfile('init.py')]
		run_in_background('update', cmd)
	elif len(wf.args):
		query = wf.args[0]
	else:
		query = None
	if is_running('update'):
		wf.add_item('In progress',
					valid=False,
					icon=ICON_INFO)
		wf.send_feedback()
		return
	try:
		variables = wf.settings["data"]
	except:
		wf.add_item(title="List not initialized",
					subtitle="You should run initVar",
					icon=ICON_ERROR)
		wf.send_feedback()
		return
	if query:
		variables = wf.filter(query, variables, key=filterVariables)
	for variable in variables:
		wf.add_item(title=variable["name"],
					subtitle=variable["value"],
					arg=variable["value"],
					valid=True,
					icon=ICON_WEB)
	wf.send_feedback()

if __name__ == "__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
