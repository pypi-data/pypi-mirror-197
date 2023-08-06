
outputname="$1"
post_date="$2"
close_date="$3"
last_month="$4"
is_excel="$5"

excel_to_csv "$last_month" "$last_month"

fed_download | fed_filter posted-date --start="$post_date" \
	| fed_filter agency-code 'HHS' --exclude \
	| fed_filter close-date --start="$close_date" \
	| fed_filter agency "U\.S\. Mission" --exclude \
	| fed_filter title "U\.S\. Mission" --exclude
	


( fed_select "tmp.txt"; )

fed_to_excel < "tmp.txt" > "${outputname}.csv"
csv_to_excel "${outputname}.csv" "${outputname}.xlsx"



