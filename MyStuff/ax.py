a = 1
b = 12
c = 14
d = 3
e = 5
mn = "qlfnl plqdm"
nm = """Sxoo xs lq wkh prqvwhu, dxwrpreloh jdqjvwd
Zlwk d edg elwfk wkdw fdph iurp Vul Odqnd
-hdk, Lbp lq wkdw Wrqnd, froru ri ZlooB Zrqnd
-rx frxog eh wkh nlqj exw zdwfk wkh Txhhq frqtxhu
RndB, iluvw wklqjv iluvw Lboo hdw Brxu eudlqv
Wkhq Lbpd vwduw urfnlqb jrog whhwk dqg idqjv
bFdxvh wkdwbv zkdw d prwkhuixfnlqb prqvwhu gr
Kdluguhvvhu iurp Plodq, wkdwbv wkh prqvwhu bgr
Prqvwhu Jlxvhssh khho, wkdwbv wkh prqvwhu vkrh
-rxqj prqhB lv wkh urvwhu dqg wkh prqvwhu fuhz
Dqg Lbp doo xs, doo xs, doo xs lq wkh edqn zlwk wkh ixqqB idfh
Dqg li Lbp idnh, L dlqbw qrwlfh bfdxvh pB prqhB dlqbw
Vr ohw ph jhw wklv vwudljkw, zdlw, Lbp wkh urrnlh?
Exw pB ihdwxuhv dqg pB vkrzv whq wlphv Brxu sdB?
IliwB N iru d yhuvh, qr doexp rxw
-hdk, pB prqhBbv vr wdoo wkdw pB Eduelhv jrwwd folpe lw
Krwwhu wkdq d Plggoh Hdvwhuq folpdwh, ylrohqw
WrqB Pdwwhukruq, gxwwB zlqh lw, zlqh lw
Qlfnl rq wkhp wlwwlhv zkhq L vljq lw
Wkdwbv krz wkhvh [wkh_ghy_lv_zklwh] vr rqhcwudfn plqghg
Exw uhdooB, uhdooB L grqbw jlyh d IcXcFcN
"Irujhw Eduelh, ixfn Qlfnl bfdxvh vkcvkhbv idnh"
"Vkh rq d glhw, " exw pB srfnhwv hdwlqb fkhhvhfdnh
Dqg Lboo vdB eulgh ri FkxfnB lv fklogbv sodB
Mxvw nloohg dqrwkhu fduhhu lwbv d plog gdB
Ehvlghv, -h, wkhB fdqbw vwdqg ehvlghv ph
L wklqn ph, Brx dqg Dpeb vkrxog péqdjh IulgdB
Slqn zlj, wklfn dvv, jlyh bhp zkls odvk
L wklqn elj, jhw fdvk, pdnh bhp eolqn idvw
Qrz orrn dw zkdw Brx mxvw vdz, wklv lv zkdw Brx olyh iru
Dk, Lbp d prwkhuixfnlqb prqvwhu
"""
def d12(s):
    global e
    cymk2 = ""
    for xyzz in s:
        cymk2 += chr((ord(xyzz) - 32 + e) % 95 + 32)
    ccc = ""
    for xyzz in cymk2:
        ccc += chr((ord(xyzz) - 32 - e) % 95 + 32)
    return ccc
def m(st,):
    cy = ""
    xy = (1 + (d + 12) + 16 + 1) - (5 * 2 * 3) - 10 // 11
    cymk = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'-"
    for dddd in st:
        if dddd in cymk:
            new_pos = (cymk.index(dddd) + xy) % len(cymk)
            cy += cymk[new_pos]
        else:
            cy += dddd

    return cy
def m1(st):
    r = []
    for xyzz in st:
        if xyzz in st:
            r.append(xyzz)
    return "".join(r)
def mmm(st):
    rr = ""
    for xyzz in st:
        if xyzz in st and xyzz != False:
            rr += xyzz
    return rr
def yyy(st):
    mmm = ""
    xy = d
    xyzzs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'-"
    for xyzz in st:
        if xyzz in xyzzs:
            ooo = (xyzzs.index(xyzz) - xy) % len(xyzzs)
            mmm += xyzzs[ooo]
        else:
            mmm += xyzz
    return mmm
def xxxxy(st):
    if d12(m1(mmm(m(st)))) == mn:
        msg =  mmm(m1(yyy(nm)))
        print(f"\u001b[32m {msg} \u001b[0m")
        return True, msg
    else:
        return False, "none"
