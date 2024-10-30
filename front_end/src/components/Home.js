// src/components/Home.js
import { Button, Combobox, ComboboxOption, ComboboxOptions, ComboboxInput, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import React, {useState} from 'react';
import { icons } from 'lucide-react';
import { Bars3Icon, BellIcon, XMarkIcon } from '@heroicons/react/24/outline'

const recipes = [
    { id: 1, title: 'Coconut cream pie' },
    { id: 2, title: 'Black bean chili' },
    { id: 3, title: 'Honey garlic chicken' },
    { id: 4, title: 'Veggie mac and cheese' },
    { id: 5, title: 'BBQ sandwich' },
  ]
  
const Home = () => {
    const [query, setQuery] = useState('');
    const [selected, setSelected] = "";

    const filteredRecipes =
        query === ''
        ? recipes
        : recipes.filter((recipes) => {
            return recipes.title.toLowerCase().includes(query.toLowerCase())
            })
    
    const [isFocused, setIsFocused] = useState(false);
    // const [query, setQuery] = useState('');

    const handleFocus = () => {
        setIsFocused(true);
        window.scrollTo(0, 0); // Scroll to the top when focused
    };

    const handleBlur = () => {
        setIsFocused(false);
    };

    // const handleChange = (event) => {
    //     setQuery(event.target.value);
    // };

    return (
        <div className="flex flex-col">
            <div className={`lg:block ${isFocused ? 'hidden': ''}`}>
                <div className="white shadow-lg flex justify-between px-5 py-4 lg:py-2">
                    <h1 className= "text-h1 uppercase text-custom-darkblue tracking-widest"> My Recipes</h1> 
                        <Menu as="menu" className="flex justify-between size-full flex-grow-0 flex-shrink-0  basis-1/4 md:basis-1/6 lg:basis-1/12">
                            <Button><icons.Plus stroke={"#2d3f5d"}/></Button>
                            <Button><icons.Filter stroke={"#2d3f5d"}/></Button>
                            <MenuButton><icons.Menu stroke={"#2d3f5d"}/></MenuButton>
                            <MenuItems>
                                <MenuItem>
                                <Button></Button>
                                </MenuItem>
                                <Button></Button>
                                <MenuItem>
                                </MenuItem>
                            </MenuItems>
                        </Menu> 
                </div>
            </div>
            <div className="w-full px-3">
            <Combobox value={selected} onChange={setSelected} onClose={() => setQuery('')}>
            <div className="w-full my-4 relative cursor-default overflow-hidden rounded-md text-left sm:text-sm">
                <icons.Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-custom-lightblue" />
                <ComboboxInput
                    className="w-full border border-custom-lightblue  focus:border-custom-blue focus:shadow-md rounded-md py-2 px-10 text-sm leading-5 text-custom-darkblue focus:ring-0 outline-none placeholder-custom-lightblue"
                    displayValue={(recipe) => recipe?.title}
                    onChange={(event) => setQuery(event.target.value)}
                    onFocus={handleFocus}
                    onBlur={handleBlur}
                    placeholder="Search"
                />
                <ComboboxOptions anchor="bottom" className="border empty:invisible">

                    {/* Add more complicated search in the future */}

                    {filteredRecipes.map((recipe) => (
                    <ComboboxOption key={recipe.id} value={recipe} className="data-[focus]:bg-blue-100">
                        {recipe.title}
                    </ComboboxOption>
                    ))}
                </ComboboxOptions>
            </div>
            </Combobox>
            </div>
        </div>
    


    // <main className="app-wrapper" >

    //     {!isFocused && (
    //     <header className="app-header bg-white p-2 px-5 text-[#2d3f5d] drop-shadow-[4px_4px_6px_rgba(113,128,150,0.5)]" >
    //         <link rel="preconnect" href="https://fonts.googleapis.com"></link>
    //         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
    //         <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet"></link>

    //         <nav class="navbar">
    //             <h1>My Recipes</h1>
    //             <ul class="menu">
    //                 <li><a href="#add-recipe"><icons.Plus /></a></li>
    //                 <li><a href="#filter"><icons.Filter /></a></li>
    //                 <li><a href="#menu"><icons.Menu /></a></li>
    //             </ul>
    //         </nav>
    //     </header>
    //     )}
    //     <main className="app-main">
    //         {/* <form class="search-bar" action="/search" method="GET">
    //             <input type="text" name="query" placeholder="Search..." required></input>
    //             <button type="submit">Search</button>
    //         </form> */}

    //         <div className="search-container">
    //             <form className={`search-bar ${isFocused ? 'fixed' : ''}`} action="/search" method="GET">
    //                 <input 
    //                     type="text" 
    //                     name="query" 
    //                     placeholder="Search..." 
    //                     value={query} 
    //                     onChange={handleChange}
    //                     onFocus={handleFocus}
    //                     onBlur={handleBlur}
    //                     required 
    //                 />
    //                 <button type="submit">Search</button>
    //             </form>
                
    //             {isFocused && (
    //                 <div className="filters">
    //                     <label>
    //                         <input type="checkbox" name="filter1" /> Filter Option 1
    //                     </label>
    //                     <label>
    //                         <input type="checkbox" name="filter2" /> Filter Option 2
    //                     </label>
    //                     <label>
    //                         <input type="checkbox" name="filter3" /> Filter Option 3
    //                     </label>
    //                 </div>
    //             )}
    //         </div>
    //     </main>
    // </main>
);

};

export default Home;