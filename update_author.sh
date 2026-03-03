#!/bin/bash

git config user.name "Archie Linux"
git config user.email "archie.linux@tech.com"
git rebase -i --root --exec "git commit --amend --no-edit --reset-author"
git log
git push -f
