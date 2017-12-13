majorProg={
            "I":["iii","vi","IV","ii","V","viio","I"],
            "ii":["V","viio","IV","ii"],
            "iii":["vi","IV","ii","V","viio","iii"],
            "IV":["V","viio","I","ii"],
            "V":["I","vi","IV","viio","ii"],
            "vi":["ii","IV","V","viio"],
            "viio":["I","V","vi","IV","ii"]
    }

minorProg={
            "i":["III","VI","iv","iio","v","VII","I"],
            "iio":["V","viio","IV","ii"],
            "III":["vi","IV","ii","V","viio","iii"],
            "iv":[],
            "v":[],
            "VI":[],
            "VII":[]
    }

chromscale=["c","c*","d","d*","e","f","f*","g","g*","a","a*","b"]

def translateRN(rn):
    rnmat={"i":0,"ii":1,"iii":2,"iv":3,"v":4,"vi":5,"vii":6}
    rn=rn.lower().replace("o","")
    return rnmat[rn]

def stripNote(note):
    if note[-1].isdigit():
        return note[:-1]
    else:
        return note

def makeChords(key):
    if key[0].islower():
        prog=minorProg
        steppattern=[2,1,2,2,1,2]
    else:
        prog=majorProg
        steppattern=[2,2,1,2,2,2]
    scale=[key.lower()]
    ind=chromscale.index(key.lower())
    for i in steppattern:
        ind+=i
        scale.append(chromscale[ind%len(chromscale)])
    chords={}
    for chord in prog.keys():
        chordnum=translateRN(chord)
        notes=[scale[chordnum],scale[(chordnum+2)%len(scale)],scale[(chordnum+4)%len(scale)]]
        chords[chord]=notes
        chordnum+=1
    return chords

def bestChord(prevchord,chords,notes,minor):
    if minor:
        candidates=minorProg[prevchord]
    else:
        candidates=majorProg[prevchord]
    bestscore=-1.
    bestchord="Memes"
    for i in candidates:
        currscore=0.
        currchord=chords[i]
        for note in notes:
            if stripNote(note[0]) in currchord:
                currscore+=note[1]
        if currscore>bestscore:
            bestscore=currscore
            bestchord=i
    return bestchord
            
def decideChords(melody,key):
    chords=makeChords(key)
    outchords=[]
    measurenotes=[]
    totbeats=0.
    i=0
    while i < len(melody):
        print(outchords)
        if totbeats < 0:
            break
        while totbeats < 1 and i < len(melody):
            totbeats+=(1./melody[i][1])
            measurenotes.append([melody[i][0],1./melody[i][1]])
            i+=1
        if len(outchords)==0:
            if key[0].islower():
                outchords.append("i")
            else:
                outchords.append("I")
        else:
            outchords.append(bestChord(outchords[-1],chords,measurenotes,key[0].islower()))
        totbeats-=1.
        if totbeats>0:
            measurenotes=measurenotes[-1]
        else:
            measurenotes=[]
    return outchords
                                        
if __name__ == "__main__":
    christmassong=[("e3",4),("f3",4),("g3",4),("e3",4),("d3",2),("c3",2),
                   ("d3",4),("e3",4),("d3",4),("g2",4),("d3",1),
                   ("e3",4),("f3",4),("g3",4),("e3",4),("d3",2),("c3",2),
                   ("d3",4),("e3",4),("d3",4),("c3",4),("c3",1)]
    christmas2ong=[("e3",4),("e3",4),("e3",2),("e3",4),("e3",4),("e3",2),
                   ("e3",4),("g3",4),("c3",4),("d2",4),("e3",1),
                   ("f3",4),("f3",4),("f3",4),("f3",4),("f3",4),("e3",4),("e3",4),("e3",4),
                   ("e3",4),("d3",4),("d3",4),("e3",4),("d3",2),("g3",2),
                   ("e3",4),("e3",4),("e3",2),("e3",4),("e3",4),("e3",2),
                   ("e3",4),("g3",4),("c3",4),("d2",4),("e3",1),
                   ("f3",4),("f3",4),("f3",4),("f3",4),("f3",4),("e3",4),("e3",4),("e3",4),
                   ("g3",4),("g3",4),("f3",4),("e3",4),("c3",1)]
    christmas3ong=[(i[0],i[1]*2) for i in christmas2ong]
    print(decideChords(christmas3ong,"a"))
