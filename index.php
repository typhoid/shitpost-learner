<?
    $boards = scandir( 'data' );
    unset( $boards[0] );    // Get rid of "."
    unset( $boards[1] );    // Get rid of ".."

    // Every board has two corresponding files: <board>-data and <board>-images
    // All we care about is the board name, so get rid of the -data file and
    // get only the board name from the -image file
    for( $i = 0; $i < count( $boards ); $i += 2 )
    {
        unset( $boards[$i + 2] );
        $boards[$i + 3] = explode( '-', $boards[$i + 3] )[0];
    }
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
                <input type="number" name="count" min="5" max="20" />
                
                <br />
                
                <input type="submit" value="Shitpost" />
            </fieldset>
        </form>
    </article>
</body>
</html>
