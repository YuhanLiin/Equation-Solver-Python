from math import sin, cos, atan, sqrt, radians, degrees

def parse(string):
    equation = string.split('+')
    xvectors = []
    yvectors = []
    for term in equation:
        rb = term.find('[')
        magnitude = float(term[:rb])
        direction = term[rb+1:-1]
        if len(direction) == 1:
            #N and E are positive
            if direction == 'n':
                yvectors.append(magnitude)
                xvectors.append(0)
            elif direction == 's':
                yvectors.append(-magnitude)
                xvectors.append(0)
            elif direction == 'e':
                xvectors.append(magnitude)
                yvectors.append(0)
            elif direction == 'w':
                xvectors.append(-magnitude)
                yvectors.append(0)
                
        else:
            angle = radians(float(direction[1:-1]))
            adj = cos(angle)*magnitude
            opp = sin(angle)*magnitude
            if direction[0] == 'n':
                yvectors.append(adj)
            elif direction[0] == 's':
                yvectors.append(-adj)
            elif direction[0] == 'e':
                xvectors.append(adj)
            elif direction[0] == 'w':
                xvectors.append(-adj)

            if direction[-1] == 'n':
                yvectors.append(opp)
            elif direction[-1] == 's':
                yvectors.append(-opp)
            elif direction[-1] == 'e':
                xvectors.append(opp)
            elif direction[-1] == 'w':
                xvectors.append(-opp)
    return xvectors, yvectors


def add(xvectors, yvectors):
    assert len(xvectors) == len(yvectors)
    xtotal = sum(xvectors)
    ytotal = sum(yvectors)
    total = sqrt(xtotal**2+ytotal**2)
    angle = round(degrees(atan(abs(ytotal)/(abs(xtotal)+0.01))),2)

    if xtotal == 0 and ytotal == 0:
        return '0'
    if xtotal > 0:
        d = '[e'+str(angle)
    elif xtotal < 0:
        d = '[w'+str(angle)
    else:
        d = '['
    if ytotal > 0:
        d += 'n]'
    elif ytotal < 0:
        d += 's]'
    else:
        d = d[:2]+']'
    return str(total)+d
        
while True:    
    print "Input directions in '[n34s]' or '[n]' format right after the vector's magnitude."
    print "Use cardinal directions and put into lower case. Addition only."
    string = raw_input("Vector expression: ")
    print '= ', add(*parse(string))
    print ''
            
