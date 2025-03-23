from graphviz import Digraph

# 创建一个有向图
dot = Digraph()
dot.attr(nodesep='0.5', ranksep='1.0', rankdir='LR')
node_width='4'
node_height='2'
font_size='35'

with dot.subgraph(name='cluster_lightblue') as c:
    c.attr(rank='max')
    c.node('Tops', 'Tops', shape='ellipse', color='#00ffbf',width=node_width, height=node_height, fontsize=font_size,style='filled,bold')
    c.node('Bottom', 'Bottom', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,fontsize=font_size, style='filled,bold')
    c.node('Color', 'Color', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,fontsize=font_size, style='filled,bold')
    c.node('Hair Style', 'Hair Style', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,
           fontsize=font_size, style='filled,bold')
    c.node('Hair Color', 'Hair Color', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,fontsize=font_size, style='filled,bold')
    c.node('Sleeve', 'Sleeve', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,
           fontsize=font_size, style='filled,bold')

with dot.subgraph(name='cluster_yellow') as y:
    y.attr(rank='same')
    y.node('Tops Bottom', 'Tops Bottom', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,
           fontsize=font_size, style='filled,bold')
    y.node('Tops Sleeve', 'Tops Sleeve', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,
           fontsize=font_size, style='filled,bold')
    y.node('Tops Color', 'Tops Color', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,
           fontsize=font_size, style='filled,bold')
    y.node('Color Sleeve', 'Color Sleeve', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,
           fontsize=font_size, style='filled,bold')
    y.node('Tops Color Sleeve', 'Tops Color Sleeve', shape='ellipse', color='#00ffbf', width=node_width, height=node_height,
           fontsize=font_size, style='filled,bold')

with dot.subgraph(name='cluster_red') as t:
    t.attr(rank='min')
    t.node('Agreeableness', 'Agreeableness', shape='ellipse', color='#ffb3b3', width=node_width, height=node_height,fontsize=font_size, style='filled,bold')



dot.edges([('Tops','Sleeve'),('Tops','Tops Bottom'),('Tops','Tops Color'),('Tops','Color Sleeve'),('Tops','Tops Color Sleeve'),('Tops','Tops Sleeve'),('Bottom','Tops Bottom'),('Tops Color','Bottom'),('Tops Color Sleeve','Bottom'),('Tops Bottom','Color'),('Color','Tops Color'),('Color','Color Sleeve'),('Color','Tops Color Sleeve'),
           ('Hair Style','Tops Color Sleeve'), ('Hair Color','Tops Color Sleeve'),('Sleeve','Tops Bottom'),('Sleeve','Tops Color'),('Sleeve','Color Sleeve'),('Sleeve','Tops Sleeve'),('Sleeve','Tops Color Sleeve'),('Tops Bottom','Tops Color'),('Tops Bottom','Color Sleeve'),('Tops Sleeve','Tops Bottom'),('Tops Bottom','Tops Color Sleeve'),
           ('Tops Color','Color Sleeve'),('Tops Color','Tops Sleeve'),('Tops Color','Tops Color Sleeve'),('Color Sleeve','Tops Sleeve'),('Color Sleeve','Tops Color Sleeve'),('Tops Sleeve','Tops Color Sleeve'),
           ('Tops','Agreeableness'),('Hair Style','Agreeableness'),('Tops Bottom','Agreeableness'),('Tops Color','Agreeableness'),('Tops Sleeve','Agreeableness')
           ])

edges=[('Tops','Sleeve'),('Tops','Tops Bottom'),('Tops','Tops Color'),('Tops','Color Sleeve'),('Tops','Tops Color Sleeve'),('Tops','Tops Sleeve'),('Bottom','Tops Bottom'),('Tops Color','Bottom'),('Tops Color Sleeve','Bottom'),('Tops Bottom','Color'),('Color','Tops Color'),('Color','Color Sleeve'),('Color','Tops Color Sleeve'),
           ('Hair Style','Tops Color Sleeve'), ('Hair Color','Tops Color Sleeve'),('Sleeve','Tops Bottom'),('Sleeve','Tops Color'),('Sleeve','Color Sleeve'),('Sleeve','Tops Sleeve'),('Sleeve','Tops Color Sleeve'),('Tops Bottom','Tops Color'),('Tops Bottom','Color Sleeve'),('Tops Sleeve','Tops Bottom'),('Tops Bottom','Tops Color Sleeve'),
           ('Tops Color','Color Sleeve'),('Tops Color','Tops Sleeve'),('Tops Color','Tops Color Sleeve'),('Color Sleeve','Tops Sleeve'),('Color Sleeve','Tops Color Sleeve'),('Tops Sleeve','Tops Color Sleeve'),
           ('Tops','Agreeableness'),('Hair Style','Agreeableness'),('Tops Bottom','Agreeableness'),('Tops Color','Agreeableness'),('Tops Sleeve','Agreeableness')
           ]
stri=''
for ed in edges:
    stri+=ed[0]+'->'+ed[1]+';'
stri=stri.replace(' ','_')
print(stri)

dot.engine = 'circo'
dot.attr(overlap='false')
# dot.render('e', format='png', cleanup=True)
