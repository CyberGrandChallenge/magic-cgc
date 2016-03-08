INCDIR=$(DESTDIR)/usr/include
ETCDIR=$(DESTDIR)/etc

all:
	@echo ""

install:
	install -d $(ETCDIR)
	install -m 644 magic $(ETCDIR)
