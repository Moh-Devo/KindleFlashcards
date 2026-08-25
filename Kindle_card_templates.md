## Front Template

```html
<div class="card-content">

    <div class="word {{PartOfSpeech}}">
        {{Front}}
    </div>

    <div class="pos">
        {{PartOfSpeech}}
    </div>

</div>
```
___

## Back Template

```html
<div class="card-content">

    <div class="word {{PartOfSpeech}}">
        {{Front}}
    </div>

    <div class="pos">
        {{PartOfSpeech}}
    </div>

    <div class="meaning">
        {{Meaning}}
    </div>

    <div class="sentence">
        {{Sentence}}
    </div>

    <div class="synonyms">
        <span class="label">Synonyms</span>
        {{Synonyms}}
    </div>

    <div class="translation">
        {{Translation}}
    </div>

</div>

<script>
const word = "{{text:Front}}";
const partOfSpeech = "{{PartOfSpeech}}";
const sentenceElement = document.querySelector(".sentence");

if (word && sentenceElement) {

    const colors = {
        noun: "#5dade2",
        verb: "#58d68d",
        adjective: "#f5b041"
    };

    const color = colors[partOfSpeech] || "#eeeeee";

    const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    const regex = new RegExp(
        `\\b(${escapedWord})\\b`,
        'gi'
    );

    sentenceElement.innerHTML =
        sentenceElement.innerHTML.replace(
            regex,
            `<span class="sentence-word" style="color: ${color}; font-weight: 700;">$1</span>`
        );
}
</script>
```
___

## Styling

```css
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    text-align: center;
    background: #1e1e1e;
    color: #eeeeee;
}

.card-content {
    max-width: 700px;
    margin: 0 auto;
    padding: 40px 25px;
}

.word {
    font-size: 52px;
    font-weight: 700;
    margin-bottom: 8px;
}

.pos {
    display: inline-block;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 35px;
    padding: 5px 12px;
    border-radius: 999px;
}

.meaning {
    font-size: 23px;
    line-height: 1.5;
    margin-bottom: 30px;
}

.sentence {
    font-size: 20px;
    line-height: 1.6;
    margin: 30px 0;
    padding: 20px;
    border-radius: 12px;
    background: #292929;
}

.sentence-word {
    font-weight: 700;
}

.synonyms {
    font-size: 17px;
    margin-top: 25px;
}

.label {
    display: block;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.6;
    margin-bottom: 6px;
}

.translation {
    font-size: 22px;
    margin-top: 30px;
    font-weight: 600;
}


/* Noun */

.word.noun {
    color: #5dade2;
}

.pos.noun {
    color: #5dade2;
    background: rgba(93, 173, 226, 0.15);
}

.noun .sentence-word {
    color: #5dade2;
}


/* Verb */

.word.verb {
    color: #58d68d;
}

.pos.verb {
    color: #58d68d;
    background: rgba(88, 214, 141, 0.15);
}

.verb .sentence-word {
    color: #58d68d;
}


/* Adjective */

.word.adjective {
    color: #f5b041;
}

.pos.adjective {
    color: #f5b041;
    background: rgba(245, 176, 65, 0.15);
}

.adjective .sentence-word {
    color: #f5b041;
}
```