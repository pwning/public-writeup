rm data.arff

cat <<EOF >> data.arff
@RELATION colors

@ATTRIBUTE class {0, 1, 2, 3, 4, 5, 6, 7}
@ATTRIBUTE hue NUMERIC
@ATTRIBUTE brightness NUMERIC
@ATTRIBUTE red NUMERIC
@ATTRIBUTE green NUMERIC
@ATTRIBUTE blue NUMERIC

@DATA
EOF
cat data.csv >> data.arff

# You need to make sure you actually have this JAR in that location, or this won't work :)
CLASSPATH=~/tmp/weka.jar java weka.classifiers.trees.J48 -C 0.25 -M 1 -doNotMakeSplitPointActualValue -num-decimal-places 3 -c 1 -t data.arff > weka.txt
node convert.js
