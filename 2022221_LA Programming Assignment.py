'''
Input format is input from file
First 2 lines contain number of rows and colums respectively.
The next lines contain the matrix.
'''

def matrixInputFromFile(f):

    x = f.readline()
    x = f.readline()

    x = f.read()
    L = x.split("\n")
    matrix = []

    for i in L:
        temp = []
        j = i.split()
        for k in j:
            temp.append(float(k))
        matrix.append(temp)
    return matrix

matrixFile = open("matrix.txt","r")
originalMatrix = matrixInputFromFile(matrixFile)

# Above code reads the matrix from file, and makes it into a list of lists.

m = len(originalMatrix)
n = len(originalMatrix[0])

#m and n represent the number of rows and columns respectively.

while True:
    i = 0
    for j in range(n):
        if i >= m:
            break
        pivot = originalMatrix[i][j] #Finding pivot columns
        if pivot == 0:
            for k in range(i+1, m):
                if originalMatrix[k][j] != 0:
                    pivot = originalMatrix[k][j]
                    copy = originalMatrix[i]
                    originalMatrix[i] = originalMatrix[k]
                    originalMatrix[k] = copy
                    break
            else:
                j = j + 1
                continue
        originalMatrix[i] = list(map(lambda a: a/pivot, originalMatrix[i]))
        for k in range(i+1, m):
            originalMatrix[k] = list(map(lambda l: originalMatrix[k][l] - originalMatrix[k][j] * originalMatrix[i][l], range(n)))
        i = i + 1
        break
    break

# The Matrix 'originalMatrix' has been modified to store the echelon form.
x = originalMatrix #X now stores echelon form 

print("Echelon form")
for i in x:
    print(i)
print()

def echelonToRREF(matrix): #Function to find RREF
    rows = len(matrix)
    cols = len(matrix[0])
    lead = 0
    for r in range(rows):
        if lead >= cols:
            return matrix
        i = r
        while matrix[i][lead] == 0:
            i =i + 1
            if i == rows:
                lead = lead +1
                i = r
                if cols == lead:
                    return matrix

        copy = matrix[i]
        matrix[i] = matrix[r]
        matrix[r] = copy
        leadingElement = matrix[r][lead]
        matrix[r] = list(map(lambda mrx: mrx / float(leadingElement), matrix[r]))
        for i in range(rows):
            if i != r:
                leadingElement = matrix[i][lead]
                matrix[i] = list(map(lambda pair: pair[1] - leadingElement * pair[0], zip(matrix[r], matrix[i])))

        lead = lead + 1

    for r in range(rows):
        lead = 0
        for c in range(cols):
            if matrix[r][c] == 1:
                lead = c
                break
        for i in range(r+1, rows):
            if matrix[i][c] != 0:
                leadingElement = matrix[i][c]
                matrix[i] = list(map(lambda pair: pair[1] - leadingElement * pair[0], zip(matrix[r], matrix[i])))
    return matrix

y = echelonToRREF(x) #y now stores the nested list which has the rref

print("RREF Form")
for i in y:
    print(i)
print()

for i in range(len(y)):
    y[i].append(0)

matrix = y

#Following is the code for parametric solution.

counter = 0
freeVariables = False
for i in range(m):
    if matrix[i] == [0]*(n+1):
        counter += 1 #Counting columns with all entries 0

    if n > m or n > counter:
        freeVariables = True

    if freeVariables:
        listCount = []
        matrixVariableCount = [L+1 for L in range(n)]
        for i in range(m):
            counter2 = 0
            for j in range(i, n): #Counting from pivot till last
                counter2 += 1
                if matrix[i][j] == 1:
                    listCount.append(i + counter2)
                    break
        freeVariablePosition = [] #List to store free-variables 
        for x in matrixVariableCount:
            if x not in listCount:
                freeVariablePosition.append(x)
        vectorList = []
        for i in freeVariablePosition:
            vectorList.append([-matrix[j][i-1] for j in range(m)])
        out = "x = "
        for i in range(len(freeVariablePosition)):
            vector = vectorList[i] #Stores the list for any particular free variable
            j = 0
            while j < len(freeVariablePosition):
                if freeVariablePosition[j] == freeVariablePosition[i]:
                    vector.insert(freeVariablePosition[j]-1, 1) #as x# would be 1 for x#
                else:
                    vector.insert(freeVariablePosition[j]-1, 0)
                j += 1

            if len(vector) > n:
                numberOfTimes = len(vector)

                for k in range(numberOfTimes -n -1):
                    vector.pop()

            for k in range(len(vector)):
                if vector[k] == -0.0:
                    vector[k] = int(vector[k])
                else:
                    vector[k] = round(vector[k], 4)

            if len(vector) == n:
                pass
            else:
                vector.pop() #Remove extra elements from the answer vector

            out += str(vector) + "x" + str(freeVariablePosition[i]) + " + " #Final answer to be printed

        answer = out[:-3] #-3 removes the extra + sign

        if answer != "x":
            print(answer)
        else:
            print("Matrix has only the trivial solution since it does not have any free variables")
        exit()

    else:
        print("Matrix has only the trivial solution since it does not have any free variables")
        exit()