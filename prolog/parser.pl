:- dynamic parent/2.
:- dynamic spouse/2.
:- dynamic male/1.
:- dynamic female/1.

% Парсит входной файл на факты, которые добавляются динамически в Prolog
parse_input_file(InputFile) :-
    open(InputFile, read, InputStream),        
    
    read_lines(InputStream),
    
    close(InputStream).

read_lines(InputStream) :-
    repeat,
    read_line_to_string(InputStream, Line),
    (   Line == end_of_file
    ->  !
    ;   nl,
        write(Line),
        process_line(Line),
        fail
    ).

read_line_to_string(InputStream, Line) :-
    read_line_to_codes(InputStream, Codes),
    (   Codes == end_of_file
    ->  Line = end_of_file
    ;   string_codes(Line, Codes)
    ).

process_line(Line) :-
    (   is_gender_line(Line)
        ->  split_name_and_gender(Line, Name, Gender),    
            add_gender_fact(Name, Gender)
        ; 
        is_spouse_line(Line)
        ->  split_names(Line, Husband, Wife, ' <-> '),
            add_spouse_fact(Husband, Wife) 
        ;
        is_parent_child_line(Line)
        ->  split_names(Line, Parent, Child, ' -> '),
            add_parent_child_fact(Parent, Child)
    ).

is_gender_line(Line) :-
    sub_atom(Line, _, _, _, '(М)');
    sub_atom(Line, _, _, _, '(Ж)').

is_spouse_line(Line) :-
    sub_atom(Line, _, _, _, '<->').

is_parent_child_line(Line) :-
    sub_atom(Line, _, _, _, '->').

split_name_and_gender(Input, Name, Gender) :-
    atom_chars(Input, Chars),

    append(NameChars, [' ', '(' | Temp], Chars),
    append(GenderChars, [')'], Temp),

    atom_chars(Name, NameChars),
    atom_chars(Gender, GenderChars).

split_names(Input, Husband, Wife, Delimiter) :-
    atomic_list_concat([Husband, Wife], Delimiter, Input).

add_gender_fact(Name, Gender) :-
    (
        Gender = 'М',
        assertz(male(Name))
    );
    (
        Gender = 'Ж',
        assertz(female(Name))
    ).

add_spouse_fact(Husband, Wife) :-
    assertz(spouse(Husband, Wife)).  

add_parent_child_fact(Parent, Child) :-
    assertz(parent(Parent, Child)).  