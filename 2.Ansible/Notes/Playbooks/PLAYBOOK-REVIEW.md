# Playbooks Review: Use Cases and Key Concepts

This document summarizes the intended use case and concepts demonstrated by each playbook in this folder.

| Playbook | Use Case | Key Concepts / Modules |
|---|---|---|
| 1.exampleplay.yml | Minimal playbook showing basic structure | Play, hosts, tasks, ansible.builtin.debug |
| 2.packageinstalltion.yml | Install and start nginx | ansible.builtin.package, ansible.builtin.service, become |
| 3.Variable.yml | Working with simple variables and type inspection | vars, Jinja2 interpolation, type_debug filter |
| 4.Varaiablewithlist.yaml | Variables with list and dict (indexing, attribute access) | Lists, dicts, Jinja2 accessors |
| 5.Varaiblefromvarsfile.yml | Load variables from external files (YAML/JSON) | vars_files, external var files (varswithjson.json, varswithyaml.yaml) |
| 6.Passingvariablefromcmdline.yml | Pass variables from CLI and understand precedence | --extra-vars (-e), variable precedence |
| 7.Readinginputfromuser.yaml | Read values at runtime interactively | vars_prompt, private input |
| 8.Registerouput.yml | Capture and reuse command output | register, command module, stdout/stderr |
| 9.Setfacts.yaml | Create/override variables during runtime | ansible.builtin.set_fact |
| 10.Arthimeticoperators.yaml | Arithmetic operations in Jinja | +, -, *, /, %, Jinja math expressions |
| 11.filterandmethod.yaml | Filters and methods usage | Jinja2 filters/methods (e.g., lower, upper, regex) |
| 12.membershipopin.yaml | Membership checks (in) | in operator, conditionals |
| 13.membershipopnotin.yaml | Membership checks (not in) | not in operator, conditionals |
| 14.logicalop.yaml | Logical operators | and, or, not |
| 14a.logicalop.yml | Logical operators (alt example) | and, or, not |
| 15.Testop.yaml | Test operators and Jinja tests | is defined/undefined, is string/number, etc. |
| 16.installpackagebasedonos.yaml | Install package based on OS family | when with ansible_facts.os_family, apt/yum selection |
| 17.stringoperations.yml | String operations and filters | string concat, length, replace, split, etc. |
| 18.whencondtion.yaml | Conditional task execution | when clauses on vars/facts |
| 19.lnlinecondtions.yaml | Inline/ternary-like conditions | Jinja ternary, default filter |
| 20.installpkgusingnodes.yaml | Install package on selected nodes/groups | Targeting inventory groups/hosts |
| 21.installpkgusingnodeandpassingvalues.yaml | Same as above + pass values | Variables + inventory targeting |
| 22.Handlers.yaml | Using handlers to react to changes | notify, handlers, service reload/restart |
| 23.Errorhandling.yaml | Error handling patterns | ignore_errors, failed_when, block/rescue |
| 24.ignoreerror.yaml | Continue even if a task fails | ignore_errors |
| 25.remotesrc.yaml | Copy/extract files that exist on remote | copy/unarchive with remote_src: true |
| 26.setupjava.yaml | Install and configure Java | package install (OpenJDK), environment setup |
| 27.asnibletags.yaml | Run selective tasks using tags | tags, --tags/--skip-tags |
| 28.loops.yaml | Loop constructs | loop/with_items, loop_control |
| 29.loopwithlistanddict.yaml | Loop over lists and dicts | dict2items, subelements |
| 30.loopwithditct.yaml | Loop over dict only | dict iteration |
| 31.Javanginxversion.yaml | Check and display versions | command/register/debug to print versions |
| 32.javanginxversionusingsetfacts.yaml | Persist version info in facts | set_fact, registered vars |
| 33.templatedemo.yaml | Render config/content from templates | ansible.builtin.template, Jinja2 |
| 34.templatemodulewithcondtions.yaml | Template with conditions and notifications | template + when + notify |
| index.j2 | Template example used by template playbooks | Jinja2 template |
| test.j2 | Template example used by template playbooks | Jinja2 template |
| varswithjson.json | Variables source (JSON) | Referenced via vars_files |
| varswithyaml.yaml | Variables source (YAML) | Referenced via vars_files |
| ansible-project/main_include.yml | Include tasks by OS | include_tasks, OS split |
| ansible-project/main_import.yml | Import tasks by OS | import_tasks (static) |
| ansible-project/tasks/debian.yml | Debian-specific tasks | OS-specific task file |
| ansible-project/tasks/redhat.yml | RedHat-specific tasks | OS-specific task file |

## Notes
- Filenames with typos are kept to match existing content; use this review to identify the intent.
- Many examples rely on inventory groups (DEV/PROD) and facts; run with a proper inventory.
- For CLI vars: ansible-playbook play.yml -e "x=10".
- For tags: ansible-playbook play.yml --tags setup --skip-tags never.
