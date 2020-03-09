

ifeq ($(OS),Windows_NT)
    TARGET_PLATFORM = WIN
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        TARGET_PLATFORM = LINUX
    endif
    ifeq ($(UNAME_S),Darwin)
        TARGET_PLATFORM = OSX
    endif
endif
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

all: env build
.phony: all

.phony: env
env:
	#$(Q)rm -rd $(DISTRIBUTION) 2>/dev/null || :
	#$(Q)rm -rd $(DESTINATION) 2>/dev/null || :
	$(Q)mkdir -p $(DESTINATION)

.phony: run
run: extern
	$(Q)cd src && python3 __init__.py

.phony: build
build: env extern
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
	# build python 3.7
	$(Q)cd build && wget -N https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz && tar xzf Python-3.7.6.tgz
	$(Q)cd build/Python-3.7.6 && ./configure --enable-framework=$(DESTINATION)/Library/Frameworks
	$(Q)cd build/Python-3.7.6 && make
	$(Q)cd build/Python-3.7.6 && make install
	$(Q)./build/bin/pip3 install PyInstaller
	# création de l'exécutable
	$(Q)./build/bin/python3 -m PyInstaller opty-spes.spec
	# création d'un dmg
	$(Q)rm -rd $(DESTINATION)/out_app
	$(Q)mkdir -p $(DESTINATION)/out_app
	$(Q)ln -s /Applications $(DESTINATION)/out_app
	$(Q)cp -avR $(DISTRIBUTION)/*.app $(DESTINATION)/out_app
	$(Q)mkdir -p $(DESTINATION)/mnt
	$(Q)rm $(DESTINATION)/tmp.dmg 2>/dev/null || :
	$(Q)hdiutil create -format UDRW -volname "Opty-Spes" -srcfolder "$(DESTINATION)/out_app" -size 100m $(DESTINATION)/tmp.dmg
	$(Q)hdiutil attach $(DESTINATION)/tmp.dmg -mountroot $(DESTINATION)/mnt
	$(Q)cp -avR $(DESTINATION)/appicon.iconset $(DESTINATION)/mnt/Opty-Spes/.VolumeIcon.icns
	$(Q)SetFile -a C $(DESTINATION)/mnt/Opty-Spes
	$(Q)hdiutil detach $(DESTINATION)/mnt/Opty-Spes
	$(Q)hdiutil convert $(DESTINATION)/tmp.dmg -format UDZO -o $(DISTRIBUTION)/opty-spes-$(VERSION)
endif
ifeq ($(TARGET_PLATFORM),LINUX)
	# création de l'exécutable
	$(Q)pyinstaller opty-spes.spec
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
endif

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