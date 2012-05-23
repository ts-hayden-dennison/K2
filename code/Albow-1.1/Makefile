VERSION := 1.1
TAR := Albow-$(VERSION)
TMP := ../$(TAR)

tar: clean
	rm -rf $(TMP)
	mkdir $(TMP)
	cp -r * $(TMP)
	(cd ..; tar -z -c -v -f $(TAR).tar.gz --exclude '.??*' $(TAR))

clean:
	rm -f */*.pyc
