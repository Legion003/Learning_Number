<?php
	// requires php5
	// 定义常量，此常量为images文件夹
	define('UPLOAD_DIR', '/var/www/html/Learning_Number/images/');
	// 接收post表单中的值
	$img = $_POST['img'];
	fwrite($std, $img);
	// 去掉'data:image/png;base64,'
	$img = str_replace('data:image/png;base64,', '', $img);
	// 把空格改为+
	$img = str_replace(' ', '+', $img);
	// base64解码
	$data = base64_decode($img);
	// 确定图片保存路径
	$file = UPLOAD_DIR . 'Legion' . '.png';
	// 把数据写入文件中，如果成功则返回写入的字符数，如果失败则返回false
	//$success = file_put_contents($file, $data);
	//file_put_contents($file, 'haha');
	$fopen = fopen($file, 'wb');
	fwrite($fopen,$data);
	fclose($fopen);
	echo $file;
	echo $data . '\n';
?>
