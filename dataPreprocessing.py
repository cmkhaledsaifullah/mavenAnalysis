import config,glob,json

def collectData(datasetfilePath):
    '''
    :param datasetfilePath: Path of the dataset for maven dataset
    The function takes each files of unit folder and pick up the class names or the method name.
    It stores the class name in the list class_data and method name in method_data
    :return: A list of class names and method names from the dataset
    '''
    files = glob.glob(datasetfilePath)
    class_data=[]
    method_data=[]
    for each_file in files:
        print("Collecting lines of ",each_file)
        each_line=open(each_file).read().strip().split('\n')
        c_data,m_data = filterUniqueClassandMethod(each_line)
        class_data.extend(c_data)
        method_data.extend(m_data)

    return class_data,method_data


def filterUniqueClassandMethod(lines):
    '''
    The function takes all lines from units.* file, then check wheather the line corresponds to a class name or a method name.
    Then return the line that represents a class name or method name
    :param lines: each lines of unit.* file
    :return: a list of class names and method names.
    '''
    print('Collecting unique class names and method names...')
    class_data = []
    method_data = []
    for each_line in lines:
        tokens = each_line.split(';')
        if len(tokens) > 10 or len(tokens) < 10:
            continue
        if tokens[1].__contains__('node'):
            continue

        if tokens[3] == '4' and tokens[1] not in class_data:
            class_data.append(tokens[1])
        elif tokens[3] == '5' and tokens[1] not in method_data:
            method_data.append(tokens[1])
    return class_data,method_data



def methodnameFixing(each_method,prevValue):
    '''
    The method takes each method name that has $constructor or $classinstance creation init. It removes the part.
    :param each_method: method name that has $constructor or $classinstance creation in it
    :param prevValue: either $constructor or $classinstancecreation
    :return: method name without $constructor or $classinstance creation
    '''
    each_method = each_method.replace(prevValue,"")
    return each_method


def methodNameProcessing(method_data):
    '''
    The function removes unneccesary and complex methods and converts constructor into its real form.
    :param method_data: a list containing all method names
    :return: A list of all method names with rectified constructor and removing unneccesary ones.
    '''

    final_methods=[]
    for each_method in method_data:
        if each_method.__contains__("$"):
            if each_method.__contains__("$constructor"):
                final_methods.append(methodnameFixing(each_method, "$constructor"))
            elif each_method.__contains__("$classInstantiation"):
                final_methods.append(methodnameFixing(each_method, "$classInstantiation"))
        else:
            final_methods.append(each_method)

    return final_methods


def writeDataset(class_data,final_methods,is_filtered):
    '''
    The function write all class names and all method names in two txt files
    :param class_data: a list of all class
    :param final_methods: a list of all methods
    :return: none
    '''
    data_file_path= ''

    if is_filtered == True:
        data_file_path = config.filtered_dataset_write_path + 'class.txt'
    else:
        data_file_path = config.full_dataset_write_path + 'class.txt'
    print('Writing Class Name at', data_file_path)
    f = open(data_file_path, "w", newline='')
    for each_class in class_data:
        f.write(each_class + '\n')

    f.close()

    if is_filtered == True:
        data_file_path = config.filtered_dataset_write_path + 'method.txt'
    else:
        data_file_path = config.full_dataset_write_path + 'method.txt'

    print('Writing Method Name at', data_file_path)
    f = open(data_file_path, "w", newline='')
    for each_method in final_methods:
        f.write(each_method + '\n')

    f.close()


def jdkClassMethod(jdkclassPath,jdkmethodPath):
    '''
    The function collects all jdk 8 class and method names from two files
    :param jdkclassPath: Path of the jdk class file
    :param jdkmethodPath: Path of the jdk method file
    :return: A list of all JDK class names and a list of all JDK method names
    '''
    jdk_class = open(jdkclassPath).read().strip().split('\n')
    jdk_method = open(jdkmethodPath).read().strip().split('\n')

    return jdk_class,jdk_method

def filteringClassMethods(fullclasspath,fullmethodpath):
    '''
    The function takes all class names and method names and then remove the duplication. It stores filtred class name
    and method names at ./dataset/filtred/ directory
    :param fullclasspath: path of the full class dataset
    :param fullmethodpath: path of the full method dataset
    :return: none
    '''
    print('Reading all classes from', fullclasspath)
    classes = open(fullclasspath).read().strip().split('\n')
    print('Number of classses before filtering:', len(classes))
    print('Class name filteration is starting....')
    final_class = []
    for each_class in classes:
        if not each_class.__contains__('(') and\
           not each_class.__contains__(')') and\
           not each_class.__contains__('$') and\
           not each_class.__contains__('#') and\
           not each_class.__contains__('/') and\
           not each_class.__contains__('.java')and\
           each_class not in final_class:
            final_class.append(each_class)

    print('Number of classses after filtering:', len(final_class))
    print('Reading all methods from', fullmethodpath)
    methods = open(fullmethodpath).read().strip().split('\n')
    print('Number of methods before filtering:', len(methods))
    print('Method name filteration is starting....')
    final_methods = []
    for each_method in methods:
        if each_method not in final_methods:
            final_methods.append(each_method)

    print('Number of methods after filtering:', len(final_methods))
    return final_class,final_methods

def duplicateClassdetection(filteredclassPath,classtopackagePath):
    '''
    The function takes the filtred class names and then create duplicate class to package name mapping type jason
    :param filteredclassPath: Path of the file containe all unique class name of maven and jdk
    :param classtopackagePath: Path of the class to packege mapping json file
    :return: none
    '''
    print('Reading filtered classes from', filteredclassPath)
    classes = open(filteredclassPath).read().strip().split('\n')
    print('Creating class to package mapping....')
    duplicate_class = {}
    for each_class in classes:
        tokens = each_class.strip().split('.')
        class_name = tokens[len(tokens) - 1]
        if class_name in duplicate_class:
            other_classes = duplicate_class[class_name]
            other_classes.append(each_class)
            duplicate_class[class_name] = other_classes
        else:
            duplicate_class[class_name] = [each_class]

    final_class_dataset = {}
    number_duplicate_class = 0
    for class_name, class_list in duplicate_class.items():
        if len(class_list) > 1:
            final_class_dataset[class_name] = class_list
            number_duplicate_class += len(class_list)

    print('Total number of classes in our Dataset:', len(classes))
    print('Total number of duplicate classes having different package:', number_duplicate_class)
    print('Total number of discreate classes in our dataset:', len(final_class_dataset))
    print('Percentage of duplicate classes in our dataset:', float(number_duplicate_class * 100 / len(classes)), '%')

    print('Writing duplicate classes to package mapping at',classtopackagePath)
    with open(classtopackagePath, "w") as write_file:
        json.dump(final_class_dataset, write_file)

def duplicateMethoddetection(classstopackagePath,classtomethodpath):
    '''
    The function takes duplicate class to package mapping json file and create a class to methods mapping json file
    :param classstopackagePath: Path of the class to package mapping json file
    :param classtomethodpath: Path of the class to method mapping json file
    :return:none
    '''
    print('Importing class to package mapping from', classstopackagePath)
    with open(classstopackagePath, "r") as read_file:
        final_class_dataset = json.load(read_file)
    print('Reading filtered methods from', config.filtered_dataset_write_path + 'method.txt')
    filepath = config.filtered_dataset_write_path + 'method.txt'
    methods = open(filepath).read().strip().split('\n')

    print('Creating class to method mapping....')
    final_method_dataset = {}
    for class_name,class_list in final_class_dataset.items():
        class_method_dict = {}
        for each_class in class_list:
            method_list = [s for s in methods if each_class+"." in s]
            method_list.extend([s for s in methods if each_class+"(" in s])
            class_method_dict[each_class]=method_list
        final_method_dataset [class_name] = class_method_dict
    print('Writing duplicate classes to methods mapping at', classtomethodpath)
    with open(classtomethodpath, "w") as write_file:
        json.dump(final_method_dataset, write_file)

def createMethodtoClassMapping(classtomethodPath,methodtoclassPath):
    '''
    The function takes the class to method mapping jason file and create a method to class mapping json file
    :param classtomethodPath: Path of the class to method mapping json file
    :param methodtoclassPath: Path of the method to class mapping json file
    :return: none
    '''
    print('Importing class to method mapping from', classtomethodPath)
    with open(classtomethodPath, "r") as read_file:
        final_methods_dataset = json.load(read_file)
    print('Creating method to class mapping....')
    methodtoclass_dict={}
    for each_class,fqns in final_methods_dataset.items():
        for each_fqn, method_list in fqns.items():
            for each_method in method_list:
                method_name = each_method[each_method.index(each_class):each_method.index('(')]
                parameterString = each_method[each_method.index('(')+1:each_method.index(')')]
                parameters = [s.strip() for s in parameterString.strip().split(',')]
                if method_name in methodtoclass_dict:
                    curr_value = methodtoclass_dict[method_name]
                    curr_value.update({each_fqn:parameters})
                    methodtoclass_dict[method_name]=curr_value
                else:
                    methodtoclass_dict[method_name]={each_fqn:parameters}

    print('Filtering the methods that belongs to single class only...')
    final_methodtoclass_mapping = {}
    number_single_methods = 0
    for each_method,fqns in methodtoclass_dict.items():
        if len(fqns) > 1:
            final_methodtoclass_mapping[each_method] = fqns
        else:
            number_single_methods +=1

    print('Number of discreate methods:',len(methodtoclass_dict))
    print('Number of methods that belongs to single class:',number_single_methods)
    print('Writing methods to class mapping at', methodtoclassPath)
    with open(methodtoclassPath, "w") as write_file:
        json.dump(final_methodtoclass_mapping, write_file)

def calulateFreqMethod(dupmethodtoclassPath):
    '''
    Calculate the frequency of the method with respect ot number of class.
    :param dupmethodtoclassPath: Path of the duplicate method to class json file
    :return: None
    '''
    print('Importing class to method mapping from', dupmethodtoclassPath)
    with open(dupmethodtoclassPath, "r") as read_file:
        method_to_class = json.load(read_file)

    frequency = [0] * 12

    for each_method, class_list in method_to_class.items():

        if len(class_list) <= 10:
            frequency[len(class_list)] += 1
        else:
            frequency[11] += 1

    for i in range(2, len(frequency)):
        print("Method having", i, "classes occure in the dataset: ", frequency[i])


def calculateFreqClass(dupclasstopackagepath,finalclasstopackagepath):
    '''
    Calculate the frequency of the duplicate class and filter out the class having less tah 5 candidates
    :param dupclasstopackagepath: path of the duplicate class to package mapping json file
    :param finalclasstopackagepath: path of the filtered class to package json file
    :return: none
    '''
    print('Importing class to package mapping from', dupclasstopackagepath)
    with open(dupclasstopackagepath, "r") as read_file:
        final_class_dataset = json.load(read_file)

    dataset = calculateclassfrequency(final_class_dataset)
    print('Writing class dataset having more than 5 packages at', finalclasstopackagepath)
    with open(finalclasstopackagepath, "w") as write_file:
        json.dump(dataset, write_file)


def packagetoclass(classtopackagePath,packagetoclassPath,filteredpackagetoclassPath):
    '''
    Create the package to class mapping json file and filter out the file that has less than 5 classes in it.
    :param classtopackagePath: path of the class to package mapping json file
    :param packagetoclassPath: path of full package to class mapping json file
    :param filteredpackagetoclassPath: path of the filtered package to class mapping json file
    :return: none
    '''
    print('Importing class to package mapping from',classtopackagePath )
    with open(classtopackagePath, "r") as read_file:
        final_class_dataset = json.load(read_file)
    print('Creating package to class mapping....')
    packagetoclass_dict = {}
    for each_class, packagelist in final_class_dataset.items():
        for each_package in packagelist:
            package = each_package.replace('.'+each_class,'')
            if package in packagetoclass_dict:
                currvalue = packagetoclass_dict[package]
                currvalue.append(each_package)
                packagetoclass_dict[package]= currvalue
            else:
                packagetoclass_dict[package] = [each_package]

    frequency = [0] * 8
    dataset = {}
    for each_package,classlist in packagetoclass_dict.items():
        if len(classlist) > 10:
            frequency[7] += 1
            dataset[each_package] = classlist
        elif len(classlist) > 5:
            frequency[6] += 1
            dataset[each_package] = classlist
        else:
            frequency[len(classlist)] += 1

    print('Number of discreate package:', len(packagetoclass_dict))

    for i in range(1, 5):
        print("Number of packages that has",i,"number of class :", frequency[i],'(',frequency[i]*100/len(packagetoclass_dict),'%)')

    print("Number of packages that has 5 to 10 number of class :", frequency[6],'(',frequency[6]*100/len(packagetoclass_dict),'%)')
    print("Number of packages that has more than 10 number of class :", frequency[7],'(',frequency[7]*100/len(packagetoclass_dict),'%)')




    print('Writing package to class mapping at', packagetoclassPath)
    with open(packagetoclassPath, "w") as write_file:
        json.dump(packagetoclass_dict, write_file)

    print('Writing methods to class mapping for the packages having more than 5 classes at', filteredpackagetoclassPath)
    with open(filteredpackagetoclassPath, "w") as write_file:
        json.dump(dataset, write_file)


def calculateclassfrequency(final_class_dataset):
    print("Total number of Classes in our Dataset:", len(final_class_dataset))
    frequency = [0] * 8
    dataset = {}
    for each_class, package_list in final_class_dataset.items():
        if len(package_list) > 10:
            frequency[7] += 1
            dataset[each_class] = package_list
        elif len(package_list) > 5:
            frequency[6] += 1
            dataset[each_class] = package_list
        else:
            frequency[len(package_list)] += 1

    for i in range(2, 5):
        print("Number of class that belongs to", i, "number of packages:", frequency[i], '(',
              frequency[i] * 100 / len(final_class_dataset), '%)')

    print("Number of class that belongs to 6-10 number of packages:", frequency[6], '(',
          frequency[6] * 100 / len(final_class_dataset), '%)')
    print("Number of class that belongs to more tham 10 number of packages:", frequency[7], '(',
          frequency[7] * 100 / len(final_class_dataset), '%)')
    return dataset


def filterClassData(classtopackagePath,packagetoclassPath,classdatasetPath):
    '''
    The function filter out the packages that are absent at filtered package to class dataset.
    Next it calculate the class dataset based on the number of candidate(packge name)
    Lastly, it filterout the classes that has less tor equal 5 candidates.
    :param classtopackagePath: path of class to package mapping json file
    :param packagetoclassPath: path of filtered package to class mapping json file
    :param classdatasetPath: path of output class dataset json file
    :return: none
    '''
    print('Importing class to package mapping from', classtopackagePath)
    with open(classtopackagePath, "r") as read_file:
        final_class_dataset = json.load(read_file)

    print('Importing package to class mapping from', config.final_dataset_path, packagetoclassPath)
    with open(packagetoclassPath, "r") as read_file:
        packagetoclass = json.load(read_file)

    filtered_class_to_package = {}

    for each_class, package_list in final_class_dataset.items():
        final_package_list = []
        for each_package in package_list:
            packageName = each_package.replace('.' + each_class, '')
            if packageName in packagetoclass:
                final_package_list.append(each_package)
        filtered_class_to_package[each_class] = final_package_list

    dataset = calculateclassfrequency(filtered_class_to_package)
    print('Writing Final Class Dataset at', classdatasetPath)
    with open(classdatasetPath, "w") as write_file:
        json.dump(dataset, write_file)

