a,b = map(int,input().strip().split())
ans = 0
if (b % a == 0) and (b!=a):
  print(1)

elif (b % a == 0) and (b==a):
  ans = 1
  print(0)

else:
  a1 , a2 = run(a) , run(b)
  x = a1 + a2
  x = list(dict.fromkeys(x))
  ans = len(x)-1
  print(ans)
  def factor(f):
      l = []
      for i in range(1,f+1):
          if f % i == 0:
              l.append(i)
      return l[-2]
  def run(r):
    t = [r]
    while True:
          
      test = t[-1]
      k = factor(test)
      t.append(k)
      if t[-1] == 1:
        break
    return t