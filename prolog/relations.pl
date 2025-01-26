:- dynamic parent/2.
:- dynamic spouse/2.
:- dynamic male/1.
:- dynamic female/1.

father(F, C) :- parent(F, C), male(F).