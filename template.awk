#
# This file parse tokens in the template and remplace them by the content file.
#
# Note: the input variable contains the content filename and output contains
# the output file name.
#

BEGIN {
	RS = "__";
	already_printed = "false";
}

/^:HEADER:$/ {
	print "<a href=\"/index.html\">davidcl</a>" >output;
	num_directories = split (output, path, "/");
        basepath = "/"
	for (i=1; i<num_directories; i++) {
		print "<a href=\"" basepath path[i] "/index.html\">" path[i] "</a>" >output;
                basepath = basepath path[i] "/";
	}
	
	name = path[num_directories];
        if (name != "index.html") {
		sub (/.html/, "", name);
		print name >output;
        }

	already_printed = "true";
}

/^:CONTENT:$/ {
	while ((getline content <input) > 0)
		print content >output;
	already_printed = "true";
}

/^:TITLE:$/ {
	# We only put the first line of text to the title
	getline content <input;
	print content >output;
	close(input)
	already_printed = "true";
}

/^:DATE:$/ {
	now = systime ();
	string = strftime ("%Y-%m-%dT%H:%M:%S", now);
	tz_offset = strftime ("%z", now);
	# Conversion from +0200 to +02:00
	string2 = substr(tz_offset, 1, 3) ":" substr(tz_offset, 4);
	print string string2 >output;
	already_printed = "true";
}

/^:HREF:$/ {
	print "/" input >output;
	already_printed = "true";
}

/^:LOCAL_CSS:$/ {
	css = gensub (/\.htm/, ".css", "g", input);
	if ((getline line <css) > 0)
		print "<link rel=\"stylesheet\" type=\"text/css\" href=\"" css "\" media=\"all\" />" >output;
	already_printed = "true";
}

{
	if (already_printed != "true")
		print $0 >output;

	already_printed = "false";
}

