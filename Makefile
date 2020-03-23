
tags=$(shell git describe --abbrev=0 --tags)
diff-version=$(shell git log --pretty=oneline HEAD...$(tags) | wc -l | sed "s/ //g")
ifneq ($(diff-version),0)
	VERSION=$(tags)-beta$(diff-version)
else
	VERSION=$(tags)
endif

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))
DESTINATION :=$(current_dir)/build
DISTRIBUTION:=$(current_dir)/dist
RESSOURCES  :=$(current_dir)/ressources
DEB=$(DESTINATION)/opty-spes-$(VERSION)
PYTHON_DIR :=$(current_dir)/extern/

V?=0

CONVERT_ARG=\( +clone  -alpha extract \
        -draw 'fill black polygon 0,0 0,100 100,0 fill white circle 100,100 100,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
     \) -alpha off -compose CopyOpacity -composite

ifeq ($(V),0)
Q=@
else
Q=
endif

OPENSSL_VERSION=1.1.1e
PYTHON_VERSION=3.7.7
PYTHON_ENV=
PYTHON=python3

ifeq ($(OS),Windows_NT)
    TARGET_PLATFORM = WIN
	TARGET_OUTPUT = zip
	PYTHON=$(PYTHON_DIR)/bin/python3
	PIP=$(PYTHON_DIR)/bin/pip3
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        TARGET_PLATFORM = LINUX
		TARGET_OUTPUT = deb
		PYTHON=$(PYTHON_DIR)/bin/python3
		PIP=$(PYTHON_DIR)/bin/pip3
    endif
    ifeq ($(UNAME_S),Darwin)
        TARGET_PLATFORM = OSX
		PYTHON=$(PYTHON_DIR)/bin/python3
		PIP=$(PYTHON_DIR)/bin/pip3
		TARGET_OUTPUT = dmg
    endif
endif

ifeq (,$(wildcard $(PYTHON)))
    PYTHON_ENV+=python
endif

all: $(TARGET_OUTPUT)
.phony: all

.phony: env
env: clean
	$(Q)echo "VERSION='$(VERSION)'" > src/VERSION.py
	$(Q)mkdir -p $(DESTINATION)
	$(Q)mkdir -p $(PYTHON_DIR)
	$(Q)mkdir -p $(DISTRIBUTION)

.phony: clean
clean:
	$(Q)rm -rd $(DESTINATION) 2>/dev/null || :

.phony: mrproper
mrproper: clean
	$(Q)rm -rd $(PYTHON_DIR) 2>/dev/null || :
	$(Q)rm -rd /src/clt/extern 2>/dev/null || :

.phony: distclean
distclean: mrproper
	$(Q)rm -rd $(DISTRIBUTION) 2>/dev/null || :


.phony: test
test: env extern $(PYTHON_ENV)
	$(Q)cd src && $(PYTHON) __init__.py

.phony: build
build: env extern $(PYTHON_ENV)
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/icon.png
ifeq ($(TARGET_PLATFORM),OSX)
	# création de l'icone pour app mac os x
	$(Q)mkdir -p $(DESTINATION)/appicon.iconset
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 16x16     $(DESTINATION)/appicon.iconset/icon_16x16.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 32x32     $(DESTINATION)/appicon.iconset/icon_16x16@2x.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 32x32     $(DESTINATION)/appicon.iconset/icon_32x32.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 64x64     $(DESTINATION)/appicon.iconset/icon_32x32@2x.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 128x128   $(DESTINATION)/appicon.iconset/icon_128x128.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 256x256   $(DESTINATION)/appicon.iconset/icon_128x128@2x.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 256x256   $(DESTINATION)/appicon.iconset/icon_256x256.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/appicon.iconset/icon_256x256@2x.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/appicon.iconset/icon_512x512.png
	$(Q)convert $(RESSOURCES)/artificial-intelligence.svg $(CONVERT_ARG) -resize 1024x1024 $(DESTINATION)/appicon.iconset/icon_512x512@2x.png
	$(Q)iconutil -c icns -o "$(DESTINATION)/appicon.icns" "$(DESTINATION)/appicon.iconset"
endif
	# création de l'exécutable
	$(Q)$(PYTHON) -m PyInstaller opty-spes.spec

.phony: extern 
extern:
	# Télécharment des dépendences extern pour une utilisation offline
	$(Q)mkdir -p src/clt/extern
	$(Q)cd src/clt/extern && wget -N https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css
	$(Q)cd src/clt/extern && wget -N https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css.map
	$(Q)cd src/clt/extern && wget -N https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js
	$(Q)cd src/clt/extern && wget -N https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js
	$(Q)cd src/clt/extern && wget -N https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js.map
	$(Q)cd src/clt/extern && wget -N https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js
	$(Q)cd src/clt/extern && wget -N https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js.map
	$(Q)cd src/clt/extern && wget -N https://use.fontawesome.com/releases/v5.12.1/js/all.js

.phony: python
python: env
	# build python $(PYTHON_VERSION) with opensll $(OPENSSL_VERSION)
	$(Q)cd build && wget -N https://www.openssl.org/source/openssl-$(OPENSSL_VERSION).tar.gz && tar zxf openssl-$(OPENSSL_VERSION).tar.gz
	$(Q)cd build && wget -N https://www.python.org/ftp/python/$(PYTHON_VERSION)/Python-$(PYTHON_VERSION).tgz && tar xzf Python-$(PYTHON_VERSION).tgz

	$(Q)cd build/openssl-$(OPENSSL_VERSION) && ./config --prefix=$(PYTHON_DIR)/openssl --openssldir=$(PYTHON_DIR)/openssl
	$(Q)cd build/openssl-$(OPENSSL_VERSION) && make -j8
	$(Q)cd build/openssl-$(OPENSSL_VERSION) && make install

ifeq ($(TARGET_PLATFORM),OSX)
	$(Q)cd build/Python-$(PYTHON_VERSION) && ./configure --enable-optimizations --with-openssl="$(PYTHON_DIR)/openssl" --enable-framework=$(PYTHON_DIR)/Library/Frameworks
else
	$(Q)cd build/Python-$(PYTHON_VERSION) && ./configure --enable-optimizations --with-openssl="$(PYTHON_DIR)/openssl" --enable-shared --prefix=$(PYTHON_DIR)
endif
	$(Q)cd build/Python-$(PYTHON_VERSION) && make -j8
	$(Q)cd build/Python-$(PYTHON_VERSION) && make install
	$(Q)$(PIP) install --upgrade pip
	$(Q)$(PIP) install -r requirements.txt

.phony: deb
deb: build
	# création du .deb pour linux
	$(Q)mkdir -p $(DEB)/DEBIAN
	$(Q)mkdir -p $(DEB)/usr/bin
	$(Q)mkdir -p $(DEB)/usr/share/applications
	$(Q)mkdir -p $(DEB)/usr/share/pixmaps
	$(Q)mv $(DISTRIBUTION)/opty-spes $(DEB)/usr/bin
	$(Q)cp $(RESSOURCES)/control $(DEB)/DEBIAN
	$(Q)cp $(RESSOURCES)/post* $(DEB)/DEBIAN 2>/dev/null || :
	$(Q)cp $(RESSOURCES)/pre* $(DEB)/DEBIAN 2>/dev/null || :
	$(Q)chmod 755 $(DEB)/DEBIAN/post* 2>/dev/null || :
	$(Q)chmod 755 $(DEB)/DEBIAN/pre* 2>/dev/null || :
	$(Q)cp $(DESTINATION)/icon.png $(DEB)/usr/share/pixmaps/opty-spes.icon.png
	$(Q)cp $(RESSOURCES)/opty-spes.desktop $(DEB)/usr/share/applications
	$(Q)sed -i "s/Version:/Version: $(subst v,,$(VERSION))/g" $(DEB)/DEBIAN/control
	$(Q)sed -i "s/Version=/Version=$(subst v,,$(VERSION))/g" $(DEB)/usr/share/applications/opty-spes.desktop
	$(Q)cd $(DESTINATION) && dpkg-deb --build opty-spes-$(VERSION) $(DISTRIBUTION)

.phony: dmg
dmg: build
	# création d'un dmg
	$(Q)mkdir -p $(DESTINATION)/out_app
	$(Q)ln -s /Applications $(DESTINATION)/out_app
	$(Q)cp -avR $(DISTRIBUTION)/*.app $(DESTINATION)/out_app
	$(Q)mkdir -p $(DESTINATION)/mnt
	$(Q)rm /tmp/tmp.dmg 2>/dev/null || :
	$(Q)hdiutil create -format UDRW -volname "Opty-Spes" -srcfolder "$(DESTINATION)/out_app" -size 100m /tmp/tmp.dmg
	$(Q)hdiutil attach /tmp/tmp.dmg -mountroot $(DESTINATION)/mnt
	$(Q)cp -avR $(DESTINATION)/appicon.iconset $(DESTINATION)/mnt/Opty-Spes/.VolumeIcon.icns
	$(Q)SetFile -a C $(DESTINATION)/mnt/Opty-Spes
	$(Q)hdiutil detach $(DESTINATION)/mnt/Opty-Spes
	$(Q)hdiutil convert /tmp/tmp.dmg -format UDZO -o $(DISTRIBUTION)/opty-spes-$(VERSION)