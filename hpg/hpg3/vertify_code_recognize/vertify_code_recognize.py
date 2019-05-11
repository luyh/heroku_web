import cv2
import queue
import os,time,sys
import numpy as np
#灰度
def _get_dynamic_binary_image(img):
    # 灰值化
    im = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 二值化
    th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)

    return th1

# 去除边框
def clear_border(img):
  h, w = img.shape[:2]
  for y in range(0, w):
    for x in range(0, h):
      if y < 2 or y > w - 2:
        img[x, y] = 255
      if x < 2 or x > h -2:
        img[x, y] = 255

  return img

# 干扰线降噪
def interference_line(img):
  h, w = img.shape[:2]
  # ！！！opencv矩阵点是反的
  # img[1,2] 1:图片的高度，2：图片的宽度
  for y in range(1, w - 1):
    for x in range(1, h - 1):
      count = 0
      if img[x, y - 1] > 245:
        count = count + 1
      if img[x, y + 1] > 245:
        count = count + 1
      if img[x - 1, y] > 245:
        count = count + 1
      if img[x + 1, y] > 245:
        count = count + 1
      if count > 2:
        img[x, y] = 255
  return img

# 点降噪
def interference_point(img, x = 0, y = 0):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    cur_pixel = img[x,y]# 当前像素点的值
    height,width = img.shape[:2]

    for y in range(0, width - 1):
      for x in range(0, height - 1):
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右上顶点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最上非顶点,6邻域
                sum = int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        elif y == width - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右下顶点
                sum = int(cur_pixel) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y - 1])

                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最下非顶点,6邻域
                sum = int(cur_pixel) \
                      + int(img[x - 1, y]) \
                      + int(img[x + 1, y]) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x + 1, y - 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            else:  # 具备9领域条件的
                sum = int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 4 * 245:
                  img[x, y] = 0
    return img

# 切割的位置
def cut_position(im):
      im_position = CFS(im)

      maxL = max(im_position[0])
      minL = min(im_position[0])

      # 如果有粘连字符，如果一个字符的长度过长就认为是粘连字符，并从中间进行切割
      if(maxL > minL + minL * 0.7):
        maxL_index = im_position[0].index(maxL)
        minL_index = im_position[0].index(minL)
        # 设置字符的宽度
        im_position[0][maxL_index] = maxL // 2
        im_position[0].insert(maxL_index + 1, maxL // 2)
        # 设置字符X轴[起始，终点]位置
        im_position[1][maxL_index][1] = im_position[1][maxL_index][0] + maxL // 2
        im_position[1].insert(maxL_index + 1, [im_position[1][maxL_index][1] + 1, im_position[1][maxL_index][1] + 1 + maxL // 2])
        # 设置字符的Y轴[起始，终点]位置
        im_position[2].insert(maxL_index + 1, im_position[2][maxL_index])

      # 切割字符，要想切得好就得配置参数，通常 1 or 2 就可以
      cropped = cutting_img(im,im_position,1,1)

      return cropped


def cfs(im,x_fd,y_fd):
  '''用队列和集合记录遍历过的像素坐标代替单纯递归以解决cfs访问过深问题
  '''

  # print('**********')

  xaxis=[]
  yaxis=[]
  visited =set()
  q = queue.Queue()
  q.put((x_fd, y_fd))
  visited.add((x_fd, y_fd))
  offsets=[(1, 0), (0, 1), (-1, 0), (0, -1)]#四邻域

  while not q.empty():
      x,y=q.get()

      for xoffset,yoffset in offsets:
          x_neighbor,y_neighbor = x+xoffset,y+yoffset

          if (x_neighbor,y_neighbor) in (visited):
              continue  # 已经访问过了

          visited.add((x_neighbor, y_neighbor))

          try:
              if im[x_neighbor, y_neighbor] == 0:
                  xaxis.append(x_neighbor)
                  yaxis.append(y_neighbor)
                  q.put((x_neighbor,y_neighbor))

          except IndexError:
              pass
  # print(xaxis)
  if (len(xaxis) == 0 | len(yaxis) == 0):
    xmax = x_fd + 1
    xmin = x_fd
    ymax = y_fd + 1
    ymin = y_fd

  else:
    xmax = max(xaxis)
    xmin = min(xaxis)
    ymax = max(yaxis)
    ymin = min(yaxis)
    #ymin,ymax=sort(yaxis)

  return ymax,ymin,xmax,xmin

def detectFgPix(im,xmax):
  '''搜索区块起点
  '''

  h,w = im.shape[:2]
  for y_fd in range(xmax+1,w):
      for x_fd in range(h):
          if im[x_fd,y_fd] == 0:
              return x_fd,y_fd

#切割字符位置
def CFS(im):
  '''切割字符位置
  '''

  zoneL=[]#各区块长度L列表
  zoneWB=[]#各区块的X轴[起始，终点]列表
  zoneHB=[]#各区块的Y轴[起始，终点]列表

  xmax=0#上一区块结束黑点横坐标,这里是初始化
  for i in range(10):

      try:
          x_fd,y_fd = detectFgPix(im,xmax)
          # print(y_fd,x_fd)
          xmax,xmin,ymax,ymin=cfs(im,x_fd,y_fd)
          L = xmax - xmin
          H = ymax - ymin
          zoneL.append(L)
          zoneWB.append([xmin,xmax])
          zoneHB.append([ymin,ymax])

      except TypeError:
          return zoneL,zoneWB,zoneHB

  return zoneL,zoneWB,zoneHB

def cutting_img(im,im_position,xoffset = 1,yoffset = 1):
    # 识别出的字符个数
    im_number = len(im_position[1])
    # 切割字符
    cropped = []
    for i in range(im_number):
        im_start_X = im_position[1][i][0] - xoffset
        im_end_X = im_position[1][i][1] + xoffset
        im_start_Y = im_position[2][i][0] - yoffset
        im_end_Y = im_position[2][i][1] + yoffset
        cropped.append(im[im_start_Y:im_end_Y, im_start_X:im_end_X])

    return cropped

def cut_img(img):
    img = img[0:30, 0:75]
    img = _get_dynamic_binary_image( img )
    img = clear_border( img )
    img = interference_line( img )
    img = interference_point( img )

    num1 = img[0:30, 5:30]
    method = img[0:30, 30:55]
    num2 = img[0:30, 55:80]

    return num1,method,num2

def sav_img(result):
        timestamp = int(time.time() * 1e6) # 为防止文件重名，使用时间戳命名文件名
        filename = "vertification_code_image/numbers/{}.jpg".format(timestamp)
        cv2.imwrite(filename, result[0])

        timestamp = int( time.time() * 1e6 )  # 为防止文件重名，使用时间戳命名文件名
        filename = "vertification_code_image/compute/{}.jpg".format( timestamp )
        cv2.imwrite( filename, result[1] )

        timestamp = int( time.time() * 1e6 )  # 为防止文件重名，使用时间戳命名文件名
        filename = "vertification_code_image/numbers/{}.jpg".format( timestamp )
        cv2.imwrite( filename, result[2] )

from hpg.hpg3.zkb_request import ZKB
def zkb_save_imgs(count=1):
    zkb = ZKB()

    for i in range(count):
        image = zkb._get_verification_code_jpg()
        result = cut_img( image )
        sav_img( result )

    time.sleep(1)

def biaozhu():
    for path in ['numbers','compute']:
        files = os.listdir( "vertification_code_image/{}".format(path) )
        for filename in files:
            filepath = 'vertification_code_image/{}/{}'.format(path,filename)
            im = cv2.imread( filepath )
            cv2.imshow(filename, im)
            key = cv2.waitKey( 0 )
            if key == 27: sys.exit()
            if key == 13: continue

            if chr(key)=='z':char = '加'
            elif chr( key ) == 'x': char = '减'
            elif chr( key ) == 'c': char = '乘'
            elif chr( key ) == 'v': char = '除'
            else:
                char = chr( key )

            print(key,char)
            filename = "vervification_code_lable/{}/{}_{}".format( path,char,filename )
            cv2.imwrite( filename, im )

import pickle
def model_train(debug = False):
    kinds = ['compute','numbers']
    models = {'compute':None,'numbers':None}
    id_label_maps = {'compute':None,'numbers':None}

    for kind in kinds:
        filenames = os.listdir( "vertify_code_recognize/vervification_code_lable/{}".format(kind) )
        samples = np.empty( (0, 900) )
        labels = []
        for filename in filenames:
            filepath = 'vertify_code_recognize/vervification_code_lable/{}/{}'.format( kind,filename )
            label = filename.split( "." )[0].split( "_" )[0]
            #print(label)
            labels.append( label )
            im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            #print(im.shape,im.size)
            roistd = cv2.resize( im, (30, 30) )
            #print( roistd.shape, roistd.size )
            sample = roistd.reshape((1, 900)).astype( np.float32 )
            samples = np.append( samples, sample, 0 )

        samples = samples.astype( np.float32 )
        unique_labels = list( set( labels ) )
        unique_ids = list( range( len( unique_labels ) ) )
        label_id_map = dict( zip( unique_labels, unique_ids ) )
        id_label_map = dict( zip( unique_ids, unique_labels ) )
        label_ids = list( map( lambda x: label_id_map[x], labels ) )
        label_ids = np.array( label_ids ).reshape( (-1, 1) ).astype( np.float32 )

        #print(type(id_label_map),id_label_map)
        with open( "vertify_code_recognize/model/{}.file".format(kind), "wb" ) as f:
            pickle.dump( id_label_map, f )

        model = cv2.ml.KNearest_create()
        model.train( samples, cv2.ml.ROW_SAMPLE, label_ids )
        model.save( "vertify_code_recognize/model/{}.yml".format(kind) )

        models[kind]=model
        id_label_maps[kind] = id_label_map

    return models,id_label_maps


def read_vertify_code(kind,cut_imgs,debug =False):

    model = cv2.ml.KNearest_create()
    fs = cv2.FileStorage( 'vertify_code_recognize/model/{}.yml'.format(kind), cv2.FileStorage_READ )
    fn = fs.getNode( "opencv_ml_knn" )
    model.read( fn )

    model.save('vertify_code_recognize/model/save_{}.yml'.format(kind))

    with open( "vertify_code_recognize/model/{}.file".format( kind ), "rb" ) as f:
        id_label_map = pickle.load( f )


    labels = []
    for img in cut_imgs:

        # im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(img.shape,img.size)
        roistd = cv2.resize( img, (30, 30) )
        # print( roistd.shape, roistd.size )
        sample = roistd.reshape( (1, 900) ).astype( np.float32 )
        ret, results, neighbours, distances = model.findNearest( sample, k=3 )
        label_id = int( results[0, 0] )
        label = id_label_map[label_id]
        if debug:
            cv2.imshow( 'img.jpg', img )
            cv2.waitKey( 0 )
            print( label )
        labels.append( label )

    return labels


def count(img,debug=False):
    num1, compute, num2 = cut_img( img )

    num1, num2 = read_vertify_code( 'numbers', cut_imgs=[num1, num2] )
    compute = read_vertify_code( 'compute', [compute] )[0]

    if debug:
        cv2.imshow('img.jpg',img)
        print( num1, compute, num2 )

    if compute == '加': return int(num1)+int(num2)
    if compute == '减': return int(num1)-int(num2)
    if compute == '乘': return int(num1)*int(num2)
    if compute == '除': return int(num1)/int(num2)


if __name__ == '__main__':

    img = cv2.imread( 'vertify_code_recognize/verificationCode.jpg' )
    cv2.imshow('origin.jpg',img)

    result = count(img,debug=True)
    print(result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()