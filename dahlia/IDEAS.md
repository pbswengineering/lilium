Dahlia
======

Dahlia is the codename for Lilium's document management app. 

I already use a Wiki to keep track of information, but I would like to
try a document management system of some sort; for some reasons that I
can't still verbalise, I feel like they would be complementary.

I have tried to evaluate some open-source alternatives, but the idea of
developing my own document management system is a compelling learning
endeavour.

Documents
---------

The central concept in Dahlia is the "document". A document is
associated to some metadata, such as:

  * An identifier
  * A category
  * A title
  * An optional description

Revisions
---------

Moreover, a document has zero or more revisions. Each revision of a
document corresponds to a file (usually a written file, but any media
could be supported, in principle) and some metadata:

  * An identifier, unique among the identifiers of the revisions of the
    same document. Consequently, to uniquely identify a specific
    revision of a document among those of all other documents, both the
    document and the revision identifiers are required.
  * A brief explanation of the reason and the content of the revision.
  
Audit trail
-----------

Dahlia keeps a detailed audit trail for all operations done on
a document and its revisions. Each record of the audit trail contains:

  * Who performed the operation
  * When the operation was performed
  * What operation was performed

Categories
----------

Each document belongs to a specific category. However, since categories
can have parents, a document will also be considered part of the
ancestor categories.