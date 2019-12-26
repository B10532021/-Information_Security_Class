import random
import hashlib

from utils import *


p_q_pairs = [
    (
        89884656743115795395424136507170634919262729460159666860546670819493535120184365809464772935891218309511639178986052254469947562627479305546095847918260500694177376981088420924641128538587921381208991479738029046111053736435855137950531468965440124993414997705949743786261407695093003207393884237448188638001,
        1190199475445108201145350205578644156255222660799
    ),
    (
        89884656743115795391259236843219390331901520853462726585773459067774260060433879788971882406904444273329661339118391497842719244866648863976273294641850228657376436272298477391421630778409760249304468435736397045203544590337305597285726533019300326057018043546046289328948957730384531078344019460311972030041,
        919918971082191023307882970330480280022432026969
    ),
    (
        89884656743115795394463121606033889560544470113005564092770044954822037856596805917383990805920753253918607786155745600903770550299419004433579793299929307994016614115624413512618143115360621577396696478497885125242688566568242322449712371415431962804924602740375202158991655181616334807801610175463188852247,
        1085586315949712835404996692403138115135546655319
    ),
    (
        89884656743115795386684049320410685088036834757043169082344132535440431058841886816780371721021576377290437612318899843299081124053141434834270967861042611524840043909366745414439154834343067131404661381399820897774562404990569909066635824348731842796782802914964586650083941928140665174341017444411483776901,
        858751503134328770063499650205087517753949508767
    ),
    (
        89884656743115795395337485379929578379068885096001660068829581202726051684811190737608731859972096615196938315815423476025076217586588209307550884328214023448327667207254079934280081008247568924009984038270026297712010220828006304965002913921288707646086169142131238813184134824279130447479604682379508485603,
        1403547920778392518402128365485659924309491926423
    ),
    (
        89884656743115795393484387071113991423881666144330444764765634118415524763589678874750271952538616686298337187369868986204117748105170857391365549929287243935902967701924255842867495373322485411956300814664157283486342423883768368398953155163879285341934332114605072103860414691218207757495399277304469684243,
        927373733600844682075838521739111356800556171399
    ),
    (
        89884656743115795392722940941860218837629620147428549457057283158541626360656476004820601381873944233840474094947470757560752615681748152898849070581642818450736887343722648932099793139931600580617705917718189218151177026467993666849940491089035791084261250956693713794582111477791373969831210704286364157607,
        994588800657311621353837267183277290601467607927
    ),
    (
        89884656743115795388996727816992771856664083041851367494120774832643751744190186231508052708953152500904022516509549612226507078590402216148153949077397179601043379595861186305063866101526216330860770456068539506441605069140146065697580478262967151765769126182822721471838167127555865241694453631393651128619,
        1449598131025955746080365690467728339142710463577
    ),
    (
        89884656743115795395192586203894166552170962757393522303980399061934505731465374397633767313266062094655757421635921694521041625318139811092396577512625794336145868734367301243162016160146625309345255933753747990223073365589285961559694708491610044693780334068601354637710772515935280669186185484231383149787,
        1236979783061797982581186405484154615771793721449
    ),
    (
        89884656743115795389514795219687924435397020145907256540696179329492440501232202697995416657705625931829862436449768582720643416972550808320603458232088992675753467199436712394453651785291719413146331317325424647295368787180640429227259885541795082887959568495537326700492375500619592016845684760140139869933,
        1332602776041548688583622290874658679091666892073
    ),
]


def generate_q():
    """
    generate the q of dsa public key
    return the seed's bit amount, seed, and q
    :return:
    """
    g = random.randrange(161, 1185)  # random generate seed's bit amount
    while (True):
        seed = random.getrandbits(g)  # random seed
        U = int(hashlib.sha1(bin(seed).encode()).hexdigest(), 16) ^ \
            int(hashlib.sha1(bin((seed + 1) % (1 << g)).encode()).hexdigest(), 16)
        q = U | (1 << 159) | 1
        if miller_rabin_test(q):
            return g, seed, q


def generate_p(seed, q, offset, g, n, L):
    """
    find the p which is L bits and p - 1 is a multiplication of q
    :param seed: random seed
    :param q: q of dsa public key
    :param offset: int
    :param g: int, seed's bit amount
    :param n: int, L//160
    :param L: int, p's bit amount
    :return:
    """
    W = 0
    for i in range(n):
        W += int(hashlib.sha1(bin((seed + offset + i) %
                                  (1 << g)).encode()).hexdigest(), 16) * (2 ** (i * 160))
    X = W + (1 << (L - 1))
    c = X % (2 * q)
    p = X - (c - 1)
    return p


def generate_p_q():
    """
    generate p, q pair, which p is 1024 bits, q is 160 bits, and q is a prime divisor of p-1
    :return: (int, int), p, q pair
    """
    L = 1024
    n = L // 160

    def initial():
        return 0, 2

    counter, offset = initial()
    q_valid = False
    while (not q_valid):
        g, seed, q = generate_q()
        while (True):
            p = generate_p(seed, q, offset, g, n, L)
            if p < (1 << (L - 1)) or not miller_rabin_test(p):
                # if p is to small or is not a prime, invalid
                counter += 1
                offset += n + 1
                if counter >= 4096:
                    # difficult to find the correspond p of q, change q
                    counter, offset = initial()
                    break
                else:
                    continue
            else:
                return (p, q)


def find_p_q():
    """
    return one of p,q pairs
    if no exist pair, generate one pair and store it
    :return: (int,int), p, q pair
    """
    if not p_q_pairs:
        p_q_pairs.append(generate_p_q())
    return p_q_pairs[random.randint(0, len(p_q_pairs) - 1)]


def generate_key():
    """
    generate public key and private key of dsa
    :return: (int, int, int, int), int
    """
    p, q = find_p_q()
    h = random.randint(2, p - 2)
    a = square_and_multiply(h, (p - 1) // q, p)
    d = random.randint(1, q - 1)
    b = square_and_multiply(a, d, p)
    return (p, q, a, b), d  # public key, private key


def generate_signature(message, public_key, private_key):
    """
    generate the signature of dsa
    message only allow byte-string, if is str the function would convert it into byte-string
    :param message: string
    :param public_key: (int, int, int, int)
    :param private_key: int
    :return: (int, int)
    """
    if type(message) == str:
        message = message.encode()
    p, q, a, b = public_key
    d = private_key
    k = random.randint(1, q - 1)
    r = square_and_multiply(a, k, p) % q % q
    s = (modulo_inverse(k, q) *
         (int(hashlib.sha1(message).hexdigest(), 16) + d * r)) % q
    return r, s


if __name__ == '__main__':
    while (True):
        print(
            "1: generate dsa key\n"
            "2: generate signature with message=\"myDSAbooo\"\n"
            "2: generate signature with input message\n"
        )
        option = int(input("select your choice:"))
        if option == 1:
            (p, q, a, b), private_key = generate_key()
            print("public key: \n\tp: {}\n\tq: {}\n\ta: {}\n\tb: {}\nprivate key: {}".format(
                p, q, a, b, private_key))
        elif option == 2:
            p = int(input("enter p of public key: "))
            q = int(input("enter q of public key: "))
            a = int(input("enter a of public key: "))
            b = int(input("enter b of public key: "))
            public_key = (p, q, a, b)
            private_key = int(input("enter private_key: "))
            message = "qwertyuiop"
            signature = generate_signature(message, public_key, private_key)
            print("signature: \n\tr: {}\n\ts: {})".format(
                signature[0], signature[1]))
        elif option == 3:
            p = int(input("enter p of public key: "))
            q = int(input("enter q of public key: "))
            a = int(input("enter a of public key: "))
            b = int(input("enter b of public key: "))
            public_key = (p, q, a, b)
            private_key = int(input("enter private_key: "))
            message = input("enter message: ")
            signature = generate_signature(message, public_key, private_key)
            print("signature: \n\tr: {}\n\ts: {})".format(
                signature[0], signature[1]))
