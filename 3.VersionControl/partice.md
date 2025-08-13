Everyday Git (solid fundamentals ) 

mkdir git-basics && cd git-basics
git init -b main
echo "*.log" > .gitignore
echo "Hello" > app.txt
git status
git add app.txt
git commit -m "feat: add app.txt"

# Change & inspect
echo "Hello v2" >> app.txt
git diff                    # diff in working tree
git add app.txt
git diff --staged           # diff of what you staged
git commit -m "feat: update app.txt to v2"

# Undo practice
git restore app.txt                 # discard working changes (before you add)
git restore --staged app.txt        # unstage (keeps file modified)


Branching & merging (FF vs no-FF)

# Fast-forward merge
git switch -c feature/greeter
echo "Hi!" > greeter.txt
git add greeter.txt && git commit -m "feat: greeter"
git switch main
git merge --ff-only feature/greeter
git branch -d feature/greeter

# No-fast-forward (keeps branch bubble in history)
git switch -c feature/tools
echo 'sum(){ echo $(($1+$2)); }' > tools.sh
git add tools.sh && git commit -m "feat: tools function"
git switch main
git merge --no-ff feature/tools -m "merge: feature/tools"
git branch -d feature/tools


Remotes, pull, push, tags

# Create repo on GitHub/GitLab first, copy URL
git remote add origin <origin-url>
git push -u origin main               # sets upstream for main

# Feature branch on remote
git switch -c feature/readme
echo "Usage" >> README.md
git add README.md && git commit -m "docs: usage"
git push -u origin feature/readme     # open a PR from the site

# Merge and tag a release
git switch main
git merge --ff-only feature/readme
git tag -a v0.1.0 -m "release: v0.1.0"
git push --follow-tags


Conflicts & resolutions (mastery) 

printf "COLOR=blue\n" > config.env
git add config.env && git commit -m "chore: base color blue"

git switch -c feature/green
echo "COLOR=green" > config.env
git commit -am "feat: theme green"

git switch main
echo "COLOR=purple" > config.env
git commit -am "feat: theme purple"

git merge feature/green        # expect conflict
# open config.env, pick a final value (e.g., COLOR=teal)
git add config.env
git commit -m "merge: resolve theme"

Fast conflict picks:

Keep “ours”: git checkout --ours config.env (then tweak if needed)

Keep “theirs”: git checkout --theirs config.env
Because rerere is enabled, similar future conflicts auto-resolve

Safe time travel & recovery

git commit --amend -m "fix: better message"   # change last commit message/content

git stash push -m "wip: idea"                  # save WIP
# do something else…
git stash pop                                  # restore WIP, remove from stash

git rebase -i HEAD~3   # interactively squash/reorder last 3 commits
git cherry-pick <sha>  # copy a specific commit onto your branch

git revert <sha>       # create a new commit that undoes <sha> (safe on shared branches)
git reset --soft HEAD~1   # move HEAD back; keep changes staged
git reset --hard HEAD~1   # discard last commit & changes (dangerous)
git reflog                 # show every HEAD move (lifesaver)
# recover from anything:
git reset --hard <good-sha-from-reflog>
