# simple wiki WIP

a simple warper for the wikipedia api 

## how to use

### install

```pip install simplewiki```

### quick start

start by setting up 
```
import simplewiki

wiki = simplewiki.wikipedia()
```
then you can get some search results
```
wiki.search("cats")
```
this will return a list of results and page ids:
```
[('Bengal cat', '63064'), ('Cat', '6678'), ('Cats, Cats, Cats!', '68799268'), ('Cats (musical)', '215013'), ('Tabby cat', '6412655')]
```
you can take one of the page ids a summarize it
```
wiki.summary(6678)
```
this will return a tuple with the title and summary 
```
('Cat', 'The cat (Felis catus) is a domestic species of small carnivorous mammal. It is the only domesticated species in the-')
```
🎉congrats you now have the wikipedia api at you fingertips

## commands

* wiki.search(str)
* wiki.summarize(int)