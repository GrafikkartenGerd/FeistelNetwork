def feistel(I,K):
    first_first = (I & 0xF000)>>12
    reversed_bitmask1 = ((first_first & 0b0001) << 3) | ((first_first & 0b0010) << 1) | ((first_first & 0b0100) >> 1) | ((first_first & 0b1000) >> 3)
    first_second = I & 0x0F00
    first_third = I & 0x00F0
    first_fourth = I & 0x000F
    reversed_bitmask4 = ((first_fourth & 0b0001) << 3) | ((first_fourth & 0b0010) << 1) | ((first_fourth & 0b0100) >> 1) | ((first_fourth & 0b1000) >> 3)

    result1 = reversed_bitmask4 << 12 | reversed_bitmask1

    s_box = [4, 3, 9, 0xa, 0xb, 2, 0xe, 1, 0xd, 0xc, 8, 6, 7, 5, 0, 0xf]

    value11 = s_box[first_second >> 8] << 8
    value12 = s_box[first_third >> 4] << 4

    result1 |= value11 | value12
    result = result1 ^ K

    return result
def network (I,K):
    Lin = I >> 16
    Rin = I & 0xFFFF

    tmp = feistel(Rin,K)
    Rout = tmp ^ Lin
    Lout = Rin << 16

    I = Rout | Lout

    return I
def encrypt(C):
    for i in range (3):
        if i == 0:
            K1 = 0x536f
            C = network(C,K1)

        if i == 1:
            K2 = 0xd2a2
            C = network(C,K2)

        if i == 2:
            K3 = 0x3e0a
            C= network(C, K3)

    return C

def reversenetwork(I,K):
    Lin = I >> 16
    Rin = I & 0xFFFF

    tmp = feistel(Lin, K) ^ Rin

    I = (tmp << 16) | Lin
    return I

def decrypt(P):
    for i in range(3):
        if i == 0:
            K3 = 0x7931
            P = reversenetwork(P, K3)

        if i == 1:
            K2 = 0x763a
            P = reversenetwork(P, K2)

        if i == 2:
            K1 = 0xd1e0
            P = reversenetwork(P, K1)

    return P

print(hex(decrypt(0x2f50d486)))
