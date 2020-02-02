
TARGET_PLATFORM?=Mac
DESTINATION?=build

V?=0

ifeq ($(TARGET_PLATFORM),Mac)
APP=$(DESTINATION)/opty-spes.app
MACOS=$(APP)/Contents/MacOS
RESSOURCES=$(APP)/Contents/Resources
CONVERT_ARG=\( +clone  -alpha extract \
        -draw 'fill black polygon 0,0 0,100 100,0 fill white circle 100,100 100,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
     \) -alpha off -compose CopyOpacity -composite
ICONUTIL=
ifneq (, $(shell which iconutil))
ICONUTIL=yes
endif
endif

ifeq ($(V),0)
Q=@
else
Q=
endif

all: env build
.phony: all

.phony: env
env:
	$(Q)rm -rd $(DESTINATION)
	$(Q)mkdir -p $(DESTINATION)

.phony: run
run:
	$(Q)cd src && ./opty-spes.sh

.phony: build
build: env
ifeq ($(TARGET_PLATFORM),Mac)
	$(Q)mkdir -p $(MACOS)
	$(Q)mkdir -p $(RESSOURCES)
	$(Q)cp -f ressources/macos/Info.plist $(APP)
	$(Q)mkdir -p $(DESTINATION)/appicon.iconset
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 16x16     $(DESTINATION)/appicon.iconset/icon_16x16.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 32x32     $(DESTINATION)/appicon.iconset/icon_16x16@2x.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 32x32     $(DESTINATION)/appicon.iconset/icon_32x32.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 64x64     $(DESTINATION)/appicon.iconset/icon_32x32@2x.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 128x128   $(DESTINATION)/appicon.iconset/icon_128x128.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 256x256   $(DESTINATION)/appicon.iconset/icon_128x128@2x.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 256x256   $(DESTINATION)/appicon.iconset/icon_256x256.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/appicon.iconset/icon_256x256@2x.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/appicon.iconset/icon_512x512.png
	$(Q)convert ressources/macos/artificial-intelligence.svg $(CONVERT_ARG) -resize 1024x1024 $(DESTINATION)/appicon.iconset/icon_512x512@2x.png
ifdef ICONUTIL
	$(Q)iconutil -c icns -o "$(RESSOURCES)/appicon.icns" "$(DESTINATION)/appicon.iconset"
else
	$(Q)rm $(DESTINATION)/appicon.iconset/icon_*@2x.png
	$(Q)png2icns "$(RESSOURCES)/appicon.icns" $(DESTINATION)/appicon.iconset/icon_*.png
endif
	$(Q)cp -fr src $(RESSOURCES)
	$(Q)echo '#!/bin/sh' > $(MACOS)/opty-spes
	$(Q)echo cd \$$\(dirname \$$0\)/../Resources/src >> $(MACOS)/opty-spes
	$(Q)echo ./opty-spes.macos >> $(MACOS)/opty-spes
	$(Q)chmod +x $(MACOS)/opty-spes
endif
