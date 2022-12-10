# ---------------------------------------------------------
# [  INCLUDES  ]
# override to whatever works on your system

include ./Makefile.in.mk


# ---------------------------------------------------------
# [  TARGETS  ]
# override to whatever works on your system


include ./Makefile.targets.mk


# ---------------------------------------------------------
# [  TARGETS  ]
# keep your targets here


.PHONY: bot.run
bot.run:
	$(PYTHON) -m samurai
