

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

DESTINATION?=build
DISTRIBUTION?=dist

VERSION=`git describe --abbrev=0 --tags`

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
	$(Q)rm -rd $(DISTRIBUTION)
	$(Q)rm -rd $(DESTINATION)
	$(Q)mkdir -p $(DESTINATION)

.phony: run
run:
	$(Q)cd src && python3 __init__.py

.phony: build
build: env
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/icon.png
ifeq ($(TARGET_PLATFORM),OSX)
	$(Q)mkdir -p $(DESTINATION)/appicon.iconset
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 16x16     $(DESTINATION)/appicon.iconset/icon_16x16.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 32x32     $(DESTINATION)/appicon.iconset/icon_16x16@2x.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 32x32     $(DESTINATION)/appicon.iconset/icon_32x32.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 64x64     $(DESTINATION)/appicon.iconset/icon_32x32@2x.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 128x128   $(DESTINATION)/appicon.iconset/icon_128x128.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 256x256   $(DESTINATION)/appicon.iconset/icon_128x128@2x.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 256x256   $(DESTINATION)/appicon.iconset/icon_256x256.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/appicon.iconset/icon_256x256@2x.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 512x512   $(DESTINATION)/appicon.iconset/icon_512x512.png
	$(Q)convert ressources/artificial-intelligence.svg $(CONVERT_ARG) -resize 1024x1024 $(DESTINATION)/appicon.iconset/icon_512x512@2x.png
 	$(Q)iconutil -c icns -o "$(DESTINATION)/appicon.icns" "$(DESTINATION)/appicon.iconset"
endif
	$(Q)pyinstaller opty-spes.spec