class Main inherits IO {
	
	out_int_IO(x : Int) : Object {
        {
			out_int(x);
        }
	};
	x : Int <- 10 * 2;
	main() : Object {
    {
        out_int_IO(10);
    }
  };
};
