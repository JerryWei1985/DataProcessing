This TN is text normalization for text. It contains three main components. The fisrt one is preprocessing. The second is engine or regular expressions processing. The last is post processing.

First step, preprocessing, processes data by regular expression befor main processing to handle some illegal characters or some specified characters for next processing.

Second step is engine or regular expression processing. Engine processing processes data by thrax fst. Regular expressions processing processes data by some ordered regular expressions. They convert all data to specified format. This is the main processing.

Third step, postprocessing, processes data by regular expressions to correct or convert some characters after main processing.

Preprocessing and postprocessing contains two regular expressions files. This is to handle some cases which can't be processed in one thread. These two steps just a mapping, and all regular expressions will be merged to one in order.

This is the first version, which pipeline is implemented by Python. Preprocessing and postprocessing are implemented by Python and main processing is implemented by C++.