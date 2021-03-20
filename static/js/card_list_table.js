$(function () {
    var num = 0;
    // idとurlセットのリストを取得
    var id_url_list = JSON.parse(document.getElementById('id_url_list').textContent);
    // 画像のurlを取得
    var img_url_list = JSON.parse(document.getElementById('image_url_list').textContent);

    if (id_url_list.length >= 6) {
        var row_num = Math.ceil(id_url_list.length/6);
        var column_num = 6;
    } else {
        var row_num = 1;
        var column_num = id_url_list.length;
    }

    // console.log(object_list);
    // console.log(row_num);
    // console.log(column_num);
    // table要素を生成
    var table = document.getElementById('card_list_table')
    for (var i = 0; i < row_num; i++) {
        // tr要素を生成
        var tr = document.createElement('tr');
        // td部分のループ
        if ( i == row_num-1 && id_url_list.length % 6 != 0) {
            column_num = id_url_list.length % 6
        }
        for (var j = 0; j < column_num; j++) {
            // td要素を生成
            var td = document.createElement('td');
            // img要素を生成
            var img = document.createElement('img');
            // imgのsrcを取得
            var src = id_url_list[num][1];
            $(img).attr('src', src);
            $(img).attr('width', 50);
            $(img).attr('height', 55);
            // a要素を生成
            var a = document.createElement('a');
            $(a).attr('href', "../card/" + id_url_list[num][0] + "/");
            a.appendChild(img);
            td.appendChild(a);
            tr.appendChild(td);
            $(tr).attr('class', 'tr')
            num++;
        }
        // tr要素をtable要素の子要素に追加
        table.appendChild(tr);
    }
    // 生成したtable要素を追加する
    // document.getElementById('card_list_table').appendChild(table);
})