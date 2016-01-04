<?
    $boards = scandir( 'data' );
    unset( $boards[0] );
    unset( $boards[1] );
?>

<html>
<head>
<title>Shitpostbot</title>
</head>
<body>
    <form method="get" id="shitpostform" action="cgi-bin/shitpost.cgi">
        <fieldset>
            <legend>Generate Shitposts</legend>
            
            Board:
            <select name="board">
                <? foreach( $boards as $board ): ?>
                    <option value="<?= $board ?>">/<?= $board ?>/</option>
                <? endforeach ?>
            </select>
            
            <br />
            
            Number of Shitposts:
            <input type="number" name="count" min="5" max="20">
            
            <br />
            <br />
            
            <input type="submit">
        </fieldset>
    </form>
</body>
</html>
