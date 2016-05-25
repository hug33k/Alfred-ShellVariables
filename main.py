# encoding: utf-8

import sys
import init
from workflow import Workflow, ICON_ERROR, ICON_INFO
from workflow.background import run_in_background, is_running

def filterVariables(variable):
	elements = []
	elements.append(variable["name"])
	elements.append(variable["value"])
	return u' '.join(elements)

def main(wf):
	if len(wf.args) and wf.args[0] == "--update" and not is_running('update'):
		cmd = ['/usr/bin/python', wf.workflowfile('init.py')]
		run_in_background('update', cmd)
	elif len(wf.args) and wf.args[0] == "--shell":
		if len(wf.args) == 2 and wf.args[1] in init.shells:
			wf.settings["shell"] = str(wf.args[1])
		else:
			for sh in init.shells:
				wf.add_item(sh,
							arg=sh,
							valid=True,
							icon=u'icon.png')
			wf.send_feedback()
			return
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
					subtitle="You should run sv init",
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
					icon=u'icon.png')
	wf.send_feedback()

if __name__ == "__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
