<?
    $boards = scandir( 'data' );
    unset( $boards[0] );
    unset( $boards[1] );
?>

<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Shitpostbot</title>
    <link rel="stylesheet" type="text/css" href="styles.css" />
</head>
<body>
    <article>
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
                
                <input type="submit">
            </fieldset>
        </form>
    </article>
</body>
</html>
