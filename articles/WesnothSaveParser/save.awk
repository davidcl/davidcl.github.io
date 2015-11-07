#
# Launch with :  zcat Modif-old.gz | gawk -f save.awk | gzip > Modif.gz
#

BEGIN {
	side_found = "";
	on_unit = "false";
	dont_print = "false";

	entete = "## Modified values";
	tab_indent = "";
	max_exp_value = "1";
	exp_value = "0";
	max_hitpoints_value = "9999";
	other_players_hitpoints = "1";

	# CONFIG
	config_sides = "1";

	# DEBUG
	DEBUG = 0;

	num_side_found = 0;
	num_max_exp_found = 0;
	num_exp_found = 0;
	num_unit_found = 0;
	not_accessable_unit = 0;
	num_max_hit_found = 0;
	num_hit_found = 0;
}

# For all brackets
/\[(\/)?[[:alnum:]]+\]/ {
	on_unit = "false";
	side_found = "";
	not_accessable_unit++;
}

# For `[unit]` expression
/\[unit\]/ {
	on_unit = "true";
	num_unit_found++;
}

# For this script `##` previous comments
/\#\#/ {
	dont_print = "true";
}

{
	if (on_unit == "true") {

		split ($1, result, "=");
		gsub (/\"/, "", result[2]);

		if (result[1] == "side" ) {
			side_found = "false";
			split (config_sides, conf_sides, " ");
			for (side in conf_sides) {
				if (result[2] == conf_sides[side]) {
					num_side_found++;
					side_found = "true";
				}
			}
		}

		if (result[1] == "max_experience") {
			num_max_exp_found++;
			max_exp = result[2];

			# special case where hand-written max_exp
			if (max_exp < 20) {
				max_exp = 20;
				reset_max_exp=1;
				dont_print="true";
			}
		}

		if (result[1] == "experience") {
			num_exp_found++;
			experience = result[2];
			dont_print = "true";
		}

		if (result[1] == "max_hitpoints") {
			num_max_hit_found++;
			max_hitpoints = result[2];
		}

		if (result[1] == "hitpoints") {
			num_hit_found++;
			hitpoints = result[2];
			dont_print = "true";
		}

		if (result[1] == "max_moves") {
			max_moves = result[2];
		}

		if (result[1] == "movement") {
			movement = result[2];
			dont_print = "true";
		}

		if (result[1] == "moves") {
			moves = result[2];
			dont_print = "true";
		}

		if (side_found == "true") {
			print tab_indent entete;

			#level up next time
			# experience = max_exp-1;

			# as seen in wesnoth/src/unit.cpp:1533,
			# if "hitpoints" is not set then it is set to the max
			hitpoints = max_hitpoints_value;

			# Set moves to max
			movement = max_moves;
			moves = max_moves;
		}

		if (side_found == "false") {
			print tab_indent "## Not modified";
			hitpoints = other_players_hitpoints;
		}

		if (side_found != "") {
			if (reset_max_exp)
				print tab_indent "max_experience=\"" max_exp "\"";
			print tab_indent "experience=\"" experience "\"";
			print tab_indent "hitpoints=\"" hitpoints "\"";
			print tab_indent "movement=\"" movement "\"";
			print tab_indent "moves=\"" moves "\"";
			side_found = "";
		}
	}

	if (dont_print != "true")
		print $0;

	dont_print = "false";
}

END {
	if (DEBUG) {
		print "num side found = " num_side_found;
		print "num max exp found = " num_max_exp_found;
		print "num exp found = " num_exp_found;
		print "num unit found = " num_unit_found;
		print "num not accessable unit found = " not_accessable_unit;
		print "num_max_hit_found = " num_max_hit_found;
		print "num_hit_found = " num_hit_found;
	}
}

