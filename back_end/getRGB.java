import java.io.File;
import java.io.IOException;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.awt.Color;

/**
 * 用于对图片进行编码
 */
public class getRGB {
    public static void main(String[] args) {
        // 读取输入的参数，此处输入的是一个base64编码的图片
        File file = new File(args[0]);
        int[][] result = null;
        int[][] rgb_mtx = null;
        int[][] rgb_scl = null;
        int[][] rgb_skl = null;

        // 当图片不存在时
        if(!file.exists()){
            System.out.println("Wrong file address!");
        }

        try{
            // 将图片读取进来
            BufferedImage bufImg = ImageIO.read(file);
            int height = bufImg.getHeight();
            int width = bufImg.getWidth();
            // 存储图片的原始数据
            result = new int[width][height];
            // 存储图片灰度化之后的数据
            rgb_mtx = new int[width][height];
            // 将图片均分为28*28份之后存储该块灰度值之和
            rgb_scl = new int[28][28];
            // 将rbg_scl的值除以100后进行存储
            rgb_skl = new int[28][28];
            String idx = "";
            String str = "";

            // TODO: ?????
            for(int i=0; i<784; i++){
                idx += "pixel" + String.valueOf(i) +",";
            }

            // 将图片灰度化
            for(int i=0; i<width; i++){
                for(int j=0; j<height; j++){
                    // getRGB返回的是ARGB，A指的是透明度，ARGB分别占用8bit
                    // 此处与0xFFFFFF作与运算是为了去除A，只剩下RGB
                    result[i][j] = bufImg.getRGB(i,j) & 0xFFFFFF;
                    Color c = new Color(result[i][j]);
                    int r = c.getRed();
                    int g = c.getGreen();
                    int b = c.getBlue();
                    // 转换为灰度图
                    int rgb = (int)((r+g+b)/3);
                    rgb_mtx[i][j] = rgb;
                }
            }

            // 将图片均分成28*28块，将每一小块的灰度值加在一起
            // 先计算第一列，再计算第二列，以此类推
            int iz = 0;
            int jz = 0;
            int seg_w = width/27;  // TODO: 这里真的不是分成了29份吗??? 不会index of out range吗???
            int seg_h = height/27;
            int wz = 0;
            int hz = 0;
            while(iz < width){
                int tmp_wdh = iz + seg_w - 1;
                while(jz < height){
                    int tmp_hgt = jz + seg_h -1;
                    // 在某一列的开头或中间
                    if(tmp_wdh < width && tmp_hgt < height){
                        for(int m=iz; m<=iz+seg_w-1; m++){
                            for(int n=jz; n<=jz+seg_h-1; n++){
                                rgb_scl[wz][hz] += rgb_mtx[m][n];
                            }
                        }
                        hz++;
                        jz += seg_h;
                    // 到该列的底部了
                    }else if(tmp_wdh < width && tmp_hgt >= height){
                        for(int m=iz; m<=iz+seg_w-1; m++){
                            // 因为接近底部所以已经不够了
                            for(int n=jz; n<=height-1; n++){
                                rgb_scl[wz][hz] += rgb_mtx[m][n];
                            }
                        }
                        break;
                    // 在最后一列
                    }else if(tmp_wdh >= width && tmp_hgt < height){
                        for(int m=iz; m<=width-1; m++){
                            for(int n=jz; n<=jz+seg_h-1; n++){
                                rgb_scl[wz][hz] += rgb_mtx[m][n];
                            }
                        }
                        hz++;
                        jz += seg_h;
                    // 到达右下角
                    }else if(tmp_wdh >= width && tmp_hgt >= height){
                        // 因为接近最右侧所以已经不够了
                        for (int m = iz; m <= width - 1; m++) {
                            for (int n = jz; n <= height - 1; n++) {
                                rgb_scl[wz][hz] += rgb_mtx[m][n];
                            }
                        }
                        break;
                    }
                }
                // 到达底部，另起一列
                wz++;
                iz += seg_w;
                if(jz >= height){
                    jz = 0;
                    hz = 0;
                }
            }

            // 将每一组灰度值除以100
            for(int i=0; i<28; i++){
                for(int j=0; j<28; j++){
                    rgb_skl[i][j] = rgb_scl[i][j] / 100;
                    str += String.valueOf(rgb_skl[i][j]) + ",";
                }
            }

            System.out.println(idx.substring(0, idx.length()-1));
            System.out.println(str.substring(0, str.length()-1));
        }catch(IOException e){
            e.printStackTrace();
        }
        

    }
}