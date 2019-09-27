# This Makefile requires the following commands to be available:
# * python
# * virtualenv
# * git
# * buildozer
# * pip3

.DEFAULT_GOAL := build

.PHONY: build


install_buildozer:
	@rm -rf buildozer/
	@git clone https://github.com/kivy/buildozer
	@cd buildozer/; python3 setup.py build; sudo pip3 install -e .; cd ..

clean:
	@rm -rf .build_incremental
	@rm -rf .buildozer

.build_incremental:
	@python3 -c "import os, re; s = re.sub('(requirements = .+?python3)','# \g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('# requirements = incremental,kivy','requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@buildozer -v android debug
	@python3 -c "import os, re; s = re.sub('# (requirements = .+?python3)','\g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('requirements = incremental,kivy','# requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@echo '1' > .build_incremental

build: .build_incremental
	@buildozer -v android debug
