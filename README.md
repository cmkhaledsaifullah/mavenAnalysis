# Maven Dataset Analysis
The repository is a python project that analyze the Maven Dataset [[1]](Refernece) with JDK 8 for duplicate classes and methods. The basic idea is to collect the class names with their package and methods where duplication in class name is detected

## Get Started
Lets consider an example: You are a Java develoepr and you copied a code fragment from a QA social platform such as stackoverflow, github isseu etc. For example, the follwoing answer from [stackoverflow](https://stackoverflow.com/questions/20157996/what-should-i-do-to-use-element-class-in-java):

```
1.  private void writeFile()
2.  {
3.    dFact = DocumentBuilderFactory.newInstance();
4.    build = dFact.newDocumentBuilder();
5.    doc = build.newDocument();
6.
7.    Element root = doc.createElement("outPutResult");
8.    doc.appendChild(root);
9.
10.   for(Result r:resultList)
11.   {
12.     Element title = doc.createElement("Title");
13.     title.appendChild(doc.createTextNode(r.getTitle));
14.     root.appendChild(title);
15.
16.     Element address = doc.createElement("Address");
17.     address.appendChild(doc.createTextNode(r.getAddress));
18.     root.appendChild(address);
19.   }
20.  }//End of Write function
```
There are couple of lines(7,12,16) where obeject of Element class is instantiated. Now there are five packages that has Element class in it:
 * javax.lang.model.element
 * javax.swing.text
 * javax.swing.text.html.parser
 * javax.xml.bind 
 * org.w3c.dom 

So, after copying the code, which package will you import? TO build a reccomendation system, we need to analyze how many times developers faces such problem. 
To do that we can either have a question survey over a buch of developer or analyze a set of such questio answer. Both process is too much time consuming. Rather we followed the third procedure.
We analyze the maven dataset[1] with JDK 8 libraries. We tried to investigate how much classes share same name with different packages. Then we collect the methods of those duplicate classes and investigate how much methods in the duplicate classes share same name.
If we able to get the statistics then we can come a conclusion about the strength of the problem described earlier.


### Contains
The project contains several python scripts by which the analysis is done.

* __main__.py: This python script initiates the analysis. User need to input one command at a time to execute each phase. All commands except coldata have prerequisite(s).
* config.py: The configuration script has all the global variables. User need to change the value of those variable before running the __main__.py scripts
* dataPreprocessing.py: It contains all the function that are used for the analysis. Each function is well documented.

There are some folders that contains specific elements for the program.
* dataset: The folder contains six more subfolder where the initial, intermediate and final data are stored
* analysisReport: The folder contains analysis report at datasetinformation.txt file.
### Requirements:
Following packages need to be installed in order to run the program:
```
python 3.5 or more
pip3
```

### Installation Step:

1. Clone the repository using following command: 
    ```
    git clone https://github.com/khaledkucse/mavenAnalysis.git
    ```
2. Download all the dataset: will be publish very shortly and put them in the dataset.

3. Changes the golbal variables in the config.py

4. Run the __main__.py file. Execute each command following the prerequisite. 


## Built With

* Python 3.6.8
## Author

* **C M Khaled Saifullah** - *Initial work* - [khaledkucse](https://github.com/khaledkucse)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

## Refernece
[1] Raemaekers, Steven, Arie van Deursen, and Joost Visser. "The maven repository dataset of metrics, changes, and dependencies." 2013 10th Working Conference on Mining Software Repositories (MSR). IEEE, 2013.