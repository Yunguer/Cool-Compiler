class Complex inherits IO {
 x : Int <- 1; -- Testar atribuição 
 y : Int; -- Testar duplicação de variavel

 init(a : Int, b : Int) : Complex {
	{
	 x = a; -- Testar comparação / Testar comparação não declarada
	 y = b;
	 self;
	}
 };

 print() : Object {
	if y = 0 -- Tetar comparação IF
	then out_int(x)
	else out_int(x).out_string("+").out_int(y).out_string("I") -- Testar chamada de tipo / Testar quantidade de parametros
	fi
 };

 reflect_0() : Complex {
	{
	 x = ~x;
	 y = ~y;
	 self;
	}
 };

 reflect_X() : Complex {
	{
	 y = ~y;
	 self;
	}
 };

};

class Complex2 inherits Complex {
    teste() : SELF_TYPE {
        (let  e : Complex2 in
	 { e.reflect_X(); -- Testar herança
	 self;}
	)
 };
};


class Main inherits IO {
 
 reflect_Y() :Main {
	{
	 self;
	}
 };
 
 main() : SELF_TYPE {
	(let c : Main, e : Complex in
	 { e.reflect_0(); -- Testar chamada de função de outra classe / Testar chamada de metodo com variavel não definida
	 if 0 = 0
	 then out_string("=)\n")
	 else out_string("=(\n")
	 fi;}
	)
 };

};

