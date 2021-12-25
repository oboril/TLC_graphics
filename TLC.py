from cairosvg import svg2png,svg2pdf

class TLC:
    def __init__(self,start=10,solvent_top=80,lanes=3,height=100,width=35):
        self.height = height;
        self.width = width;
        self.lanes = lanes;
        self.start = start;
        self.solvent_top = solvent_top;
        self.spots=[];
        self.lane_names=['']*lanes;
        self.lane_fontsize=10;
        return;
    
    def set_lane_names(self,lane_names, fontsize=10):
        if len(lane_names) != self.lanes:
            raise Exception('Incorrect number of lanes');
        self.lane_names = lane_names;
        self.lane_fontsize=fontsize;
        return;

    def spot(self,lane,distance,width=3,height=None,color='#555555'):
        """Adds spot to the TLC

        The stretch can be any value between -1 and 1. Negative values represent
        wide spots, positive values represent stretched spots.
        """
        if not height:
            height = width;
        self.spots.append({'dist':distance,'lane':lane,'width':width,
                           'height':height,'color':color});
        return;
    
    def get_Rf(self):
        Rfs = []
        for spot in self.spots:
            Rfs.append(spot['dist']/self.solvent_top);

        return Rfs;

    def save_svg(self,path):
        with open(path, 'w') as f:
            f.write(self.plot());
        return;
    
    def save_pdf(self,path):
        svg2pdf(bytestring=self.plot(),write_to=path)
        return;
    
    def save_png(self,path,dpi=96):
        svg2png(bytestring=self.plot(),write_to=path,dpi=dpi)
        return;

    def plot(self):
        """Creates a SVG string containing a sketch of the TLC plate
        
        In jupyter notebook, the content can be displayed using:

        from IPython.display import SVG, display
        
        display(SVG(tlc.plot()))

        To save the graphics to a file, use one of: save_svg(), save_pdf(), save_png()
        """
        svg_header =  '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n' \
                      '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" ' \
                      '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' \
                     f'<svg width="{self.width+10}mm" height="{self.height+10}mm" ' \
                      'xmlns="http://www.w3.org/2000/svg" ' \
                      'xmlns:xlink= "http://www.w3.org/1999/xlink">';
        svg_footer = '</svg>'

        elements = []
        elements.append(
            f'<rect x="5mm" y="5mm" width="{self.width}mm" height="{self.height}mm" '
             'fill="none" stroke="#777777" stroke-width="0.3mm"/>')

        elements.append(
            f'<line x1="5mm" y1="{5+self.height-self.start}mm"'
            f' x2="{self.width+5}mm" y2="{5+self.height-self.start}mm"'
            f' stroke-width="0.3mm" stroke="#777777" />')

        elements.append(
            f'<line x1="5mm" y1="{5+self.height-self.solvent_top-self.start}mm"'
            f' x2="{self.width+5}mm" y2="{5+self.height-self.solvent_top-self.start}mm"'
            f' stroke-width="0.3mm" stroke="#777777" />')
        
        for spot in self.spots:
            rx=spot['width']/2
            ry=spot['height']/2
            cx = 5+self.width/(self.lanes)*(spot['lane']+0.5)
            cy = 5+self.height - self.start-spot['dist']
            color = spot['color']

            elements.append(f'<ellipse cx="{cx}mm" cy="{cy}mm" rx="{rx}mm" ry="{ry}mm" '
                            f'fill="{color}" />')

        for idx,lane in enumerate(self.lane_names):
            x = 5+self.width/(self.lanes)*(idx+0.5)
            y = 5+self.height - self.start/2
            
            tspans = '\n'
            lines = lane.split('\n');
            dy=-(len(lines)-1)/2*1.2;
            for i,line in enumerate(lines):
                if line.replace(' ', '') == '':
                    dy +=1.2;
                else:
                    tspans +=f'<tspan x="{x}mm" dy="{dy}em">{line}</tspan>\n'
                    dy=1.2;
                
            

            elements.append(f'<text x="{x}mm" y="{y}mm" '
                            f'font-size="{self.lane_fontsize}pt" dominant-baseline="middle" text-anchor="middle">'
                            f'{tspans}</text>')

        text = svg_header;
        for el in elements:
            text += '\n'+el;
        text += '\n'+svg_footer;
        return text;
