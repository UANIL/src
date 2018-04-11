# Network Intrusion Lab Intern Repository
![https://cybercrime.as.ua.edu/resources/jectf/](https://cybercrime.as.ua.edu/wp-content/uploads/2015/11/Logo-2-300x269.jpg)

In this repository you will find a variety tools and programs developed in conjunction with the University of Alabama's [Joint Electronic Crimes Task Force](https://cybercrime.as.ua.edu/resources/jectf/) and Network Intrusion Lab by undergraduate student interns. Please direct all questions or concerns to the JECTF's academic coordinator, [Dr. Diana Dolliver](https://cj.ua.edu/profiles/diana-dolliver/) - DLDolliver@ua.edu.

<h2> Tools utilized </h2> 

- [Wireshark](https://www.wireshark.org/)

<h2> SQL_Parser.py </h2> 

Parser designed to sort through raw SQL statements/text and output matches based on selected keyword. Exports results to CSV file format.

</br>
</br>

<h2> URLParser.py </h2> 

Parser designed to pull URLs from a Wireshark-exported CSV file.

</br>
</br>

<h2> csvparse.py </h2>

Parser designed to organize URLs, frequency of visit, and access timestamps from Wireshark-exported CSV files.

</br>
</br>

<h2> dataFinder.py </h2> 

Tool to determine a given table's format, find an example of the output, and work for a specific table or all table names.

</br>
</br>

<h2> getHeaders.py </h2> 

Script designed to check HTTP Status Codes from CSV-stored URLs. Should those URLs exist based on the returned HTTP Status Code, it will return the header information and export results to a CSV file `header_info.csv`.
