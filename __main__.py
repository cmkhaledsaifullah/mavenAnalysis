import config,dataPreprocessing


config.init()


choice = input("Enter one of the mode: \n"
            " coldata : Collect Dataset \n"
            " filterdata: Filter duplicate class  (Prerequisite: coldata)\n"
            " dupclassdet: Collecting Duplicate class names (Prerequisite: filterdata)\n"
            " caldupclassfreq: Calculating the frequency of class (Prerequisite: dupclassdet)\n"
            " packagetoclass: Create package to class mapping from full dataset (Prerequisite: caldupclassfreq)\n"
            " dupmethoddet: Collecting Duplicate method names (Prerequisite: dupclassdet)\n"
            " methodtoclass: Creating method to class names mapping (Prerequisite: dupmethoddet)\n"
            " caldupmethodfreq: Calculating the frequency of methods (Prerequisite: methodtoclass)\n"
            " filterclassdata: Filter the classes that has packages having more than 5 classes in it (Prerequisite: caldupclassfreq,packagetoclass )\n"
            " writefinaldataset: Final Dataset after all analysis (Prerequisite: filterclassdata)\n")

if choice.strip().lower()  == 'coldata':
    jdk_class_file = config.jdk_dataset_path+'ClassName.txt'
    jdk_method_file = config.jdk_dataset_path+'MethodName.txt'
    jdk_class, jdk_method = dataPreprocessing.jdkClassMethod(jdk_class_file,jdk_method_file)

    class_data,method_data = dataPreprocessing.collectData(config.maven_dataset_units_path+"/*")

    final_methods= dataPreprocessing.methodNameProcessing(method_data)
    class_data.extend(jdk_class)
    final_methods.extend(jdk_method)

    dataPreprocessing.writeDataset(class_data,final_methods,False)

elif choice.strip().lower() == 'filterdata':
    fullclasspath = config.full_dataset_write_path + 'class.txt'
    fullmethodpath = config.full_dataset_write_path + 'method.txt'
    final_class,final_methods = dataPreprocessing.filteringClassMethods(fullclasspath,fullmethodpath)
    dataPreprocessing.writeDataset(final_class,final_methods,True)

elif choice.strip().lower() == 'dupclassdet':
    filtered_class_path = config.filtered_dataset_write_path + 'class.txt'
    dataPreprocessing.duplicateClassdetection(filtered_class_path,config.duplicate_classtopackage_path)

elif choice.strip().lower() == 'dupmethoddet':
    dataPreprocessing.duplicateMethoddetection(config.duplicate_classtopackage_path,config.duplicate_classtomethod_path)

elif choice.strip().lower() == 'methodtoclass':
    dataPreprocessing.createMethodtoClassMapping(config.duplicate_classtomethod_path,config.duplicate_methodtoclass_path)

elif choice.strip().lower() == 'caldupmethodfreq':
    dataPreprocessing.calulateFreqMethod(config.duplicate_methodtoclass_path)
    #dataPreprocessing.calulateFreqMethod(config.final_dataset_path + 'method.json')

elif choice.strip().lower() == 'caldupclassfreq':
    classtopackagePath = config.final_dataset_path+'classtopackage.json'
    dataPreprocessing.calculateFreqClass(config.duplicate_classtopackage_path,classtopackagePath)

elif choice.strip().lower() == 'packagetoclass':
    classtopackagePath = config.final_dataset_path+'classtopackage.json'
    packagetoclassPath = config.final_dataset_path+'packagetoclass.json'
    filteredpackagetoclassPath = config.final_dataset_path + 'filtredpackagetoclass.json'
    dataPreprocessing.packagetoclass(classtopackagePath,packagetoclassPath,filteredpackagetoclassPath)

elif choice.strip().lower() == 'filterclassdata':
    classtopackagePath = config.final_dataset_path + 'classtopackage.json'
    packagetoclassPath = config.final_dataset_path + 'filtredpackagetoclass.json'
    classdataset = config.final_dataset_path + 'class.json'
    dataset = dataPreprocessing.filterClassData(classtopackagePath,packagetoclassPath,classdataset)

elif choice.strip().lower() == 'writefinaldataset':
    classdataset = config.final_dataset_path + 'class.json'
    packagetoclassPath = config.final_dataset_path + 'package.json'
    filteredpackagetoclassPath = config.final_dataset_path + 'finalfiltredpackagetoclass.json'
    dataPreprocessing.packagetoclass(classdataset, packagetoclassPath, filteredpackagetoclassPath)

    classtomethodPath = config.final_dataset_path + 'finalclasstomethod.json'
    dataPreprocessing.duplicateMethoddetection(classdataset,
                                               classtomethodPath)

    methoddatasetPath = packagetoclassPath = config.final_dataset_path + 'method.json'
    dataPreprocessing.createMethodtoClassMapping(classtomethodPath,
                                                 methoddatasetPath)



