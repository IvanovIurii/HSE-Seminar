:- dynamic parent/2.
:- dynamic spouse/2.
:- dynamic male/1.
:- dynamic female/1.

married(X, Y) :-
     \+ spouse(X, Y) -> spouse(Y, X) ; spouse(X, Y).

father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M) ; father(F, C), wife(M, F).
child(C, P) :- parent(P, C).
son(S, P) :- child(S, P), male(S).
daughter(D, P) :- child(D, P), female(D).

grandparent(GP, C) :- parent(GP, P), parent(P, C).
grandfather(GF, C) :- grandparent(GF, C), male(GF).
grandmother(GM, C) :- grandparent(GM, C), female(GM).

grandchild(GC, GP) :- parent(P, GC), parent(GP, P).
grandson(GS, GP) :- grandchild(GS, GP), male(GS).
granddaughter(GD, GP) :- grandchild(GD, GP), female(GD).

sibling(A, B) :- parent(P, A), parent(P, B), A \= B.
brother(B, S) :- sibling(B, S), male(B).
sister(S, B) :- sibling(S, B), female(S).

aunt(A, N) :- sister(A, P), parent(P, N).
aunt_in_law(A, N) :- wife(A, U), brother(U, P), parent(P, N).
uncle(U, N) :- brother(U, P), parent(P, N).
uncle_in_law(U, N) :- husband(U, A), sister(A, P), parent(P, N).

nephew(N, A) :- child(N, P), sibling(P, A), male(N).
niece(N, A) :- child(N, P), sibling(P, A), female(N).

husband(H, W) :- married(H, W), male(H).
wife(W, H) :- married(H, W), female(W).

father_in_law(FIL, P) :- parent(FIL, S), married(S, P), male(FIL).
mother_in_law(MIL, P) :- parent(MIL, S), married(S, P), female(MIL). 

son_in_law(SIL, P) :- married(SIL, D), child(D, P), male(SIL).
daughter_in_law(DIL, P) :- married(DIL, S), child(S, P), female(DIL).

dever(D, W) :- brother(D, H), married(H, W).    % Деверь (брат мужа)
shurin(S, H) :- brother(S, W), married(W, H).   % Шурин (брат жены)

zolovka(Z, W) :- sister(Z, H), married(H, W).        % Золовка (сестра мужа)
svoyachinitza(S, H) :- sister(S, W), married(W, H).  % Свояченица (сестра жены)

relatives(Name, Relatives) :-
    findall(Rel, (
        father(F, Name), Rel = father(F, Name);
        mother(M, Name), Rel = mother(M, Name);
        son(C, Name), Rel = son(C, Name);
        daughter(C, Name), Rel = daughter(C, Name);
        brother(B, Name), Rel = brother(B, Name);
        sister(S, Name), Rel = sister(S, Name);
        husband(H, Name), Rel = husband(H, Name);
        wife(W, Name), Rel = wife(W, Name);
        uncle(U, Name), Rel = uncle(U, Name);
        uncle_in_law(U, Name), Rel = uncle_in_law(U, Name);
        aunt(A, Name), Rel = aunt(A, Name);
        aunt_in_law(A, Name), Rel = aunt_in_law(A, Name);
        grandfather(GF, Name), Rel = grandfather(GF, Name);
        grandmother(GM, Name), Rel = grandmother(GM, Name);
        grandson(GС, Name), Rel = grandson(GС, Name);
        granddaughter(GС, Name), Rel = granddaughter(GС, Name);
        son_in_law(SIL, Name), Rel = son_in_law(SIL, Name);
        daughter_in_law(DIL, Name), Rel = daughter_in_law(DIL, Name);
        father_in_law(FIL, Name), Rel = father_in_law(FIL, Name);
        mother_in_law(MIL, Name), Rel = mother_in_law(MIL, Name);
        nephew(N, Name), Rel = nephew(N, Name);
        niece(N, Name), Rel = niece(N, Name);
        dever(D, Name), Rel = dever(D, Name);
        shurin(S, Name), Rel = shurin(S, Name);
        zolovka(Z, Name), Rel = zolovka(Z, Name);
        svoyachinitza(S, Name), Rel = svoyachinitza(S, Name)
    ), RelList),
    list_to_set(RelList, Relatives).

% Запрос пользователю
ask_user :-
    write('Введите команду ("help." для списка команд): '), nl,
    read(Command),
    process_command(Command),
    ask_user.

% Обработка команд    
process_command(add_male(Name)) :-
    assertz(male(Name)),
    write('Человек добавлен: '), write(Name), write(', (М)'), nl.

process_command(add_female(Name)) :-
    assertz(female(Name)),
    write('Человек добавлен: '), write(Name), write(', (Ж)'), nl.

process_command(add_relation(parent, Parent, Child)) :-
    assertz(parent(Parent, Child)),
    write('Добавлена связь: '), write(Parent), write(' - родитель '), write(Child), nl.

process_command(add_relation(spouse, Spouse1, Spouse2)) :-
    assertz(spouse(Spouse1, Spouse2)),
    assertz(spouse(Spouse2, Spouse1)),
    write('Добавлена связь: '), write(Spouse1), write(' и '), write(Spouse2), write(' - супруги'), nl.

process_command(query_relatives(Name)) :-
    relatives(Name, Relatives),
    write('Родственники для '), write(Name), write(': '), nl,
    format_relatives(Relatives).

process_command(help) :-
    write('Доступные команды:'), nl,
    write('1. "add_male(Name)." - добавить человека мужского пола'), nl,
    write('2. "add_female(Name)." - добавить человека женского пола'), nl,
    write('3. "add_relation(parent, Parent, Child)." - добавить связь "родитель"'), nl,
    write('4. "add_relation(spouse, Spouse1, Spouse2)." - добавить связь "супруги"'), nl,
    write('5. "query_relatives(Name)." - запросить список родственников'), nl,
    write('6. "help." - показать список команд'), nl,
    write('7. "exit." - завершить программу'), nl.

process_command(exit) :-
    write('Завершаю работу программы...'), nl,
    halt.    

process_command(_) :-
    write('Неизвестная команда. Введите help для помощи.'), nl.

format_relatives([]).
format_relatives([Relation | Rest]) :-
    Relation =.. [RelationType, Person, _],
    write(Person), write(' - '), write(RelationType), nl,
    format_relatives(Rest).