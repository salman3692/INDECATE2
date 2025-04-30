import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import data from './pareto_data.json';

const ParetoPlot = () => {
  const svgRef = useRef();
  const [year, setYear] = useState("2040");

  useEffect(() => {
    const svg = d3.select(svgRef.current);

    const width = 800;
    const height = 600;
    const margin = { top: 90, right: 30, bottom: 60, left: 80 };

    const allX = ["2025", "2030", "2040", "2050"].flatMap(y =>
      data.map(d => d[y]).filter(v => v !== undefined && !isNaN(v))
    );

    const x = d3.scaleLinear()
      .domain([Math.min(...allX) - 20, Math.max(...allX) + 20])
      .nice()
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain([d3.min(data, d => d.EI) - 0.1, d3.max(data, d => d.EI) + 0.1])
      .range([height - margin.bottom, margin.top]);

    const color = d3.scaleSequential(d3.interpolateTurbo)
      .domain(d3.extent(data, d => d.Spec_Energy));

    let tooltip = d3.select("#tooltip");
    if (tooltip.empty()) {
      tooltip = d3.select("body")
        .append("div")
        .attr("id", "tooltip")
        .style("position", "absolute")
        .style("background", "#fff")
        .style("padding", "6px 10px")
        .style("border", "1px solid #ccc")
        .style("border-radius", "5px")
        .style("pointer-events", "none")
        .style("font-size", "15px")
        .style("font-family", "'Familjen Grotesk', sans-serif")
        .style("display", "none");
    }

    svg.selectAll(".x-axis").data([0]).join("g")
      .attr("class", "x-axis")
      .attr("transform", `translate(0, ${height - margin.bottom})`)
      .transition().duration(1000)
      .call(d3.axisBottom(x));
    svg.select(".x-axis")
      .selectAll("text")
      .style("font-size", "14px")
      .style("font-family", "'Familjen Grotesk', sans-serif");

    svg.selectAll(".y-axis").data([0]).join("g")
      .attr("class", "y-axis")
      .attr("transform", `translate(${margin.left}, 0)`)
      .transition().duration(1000)
      .call(d3.axisLeft(y));
    svg.select(".y-axis")
      .selectAll("text")
      .style("font-size", "14px")
      .style("font-family", "'Familjen Grotesk', sans-serif");

    svg.selectAll(".x-top").data([0]).join("g")
      .attr("class", "x-top")
      .attr("transform", `translate(0, ${margin.top})`)
      .call(d3.axisTop(x).tickSize(0).tickFormat(""));

    svg.selectAll(".y-right").data([0]).join("g")
      .attr("class", "y-right")
      .attr("transform", `translate(${width - margin.right}, 0)`)
      .call(d3.axisRight(y).tickSize(0).tickFormat(""));

    svg.selectAll(".xlabel").data([0]).join("text")
      .attr("class", "xlabel")
      .attr("x", width / 2)
      .attr("y", height - 15)
      .attr("text-anchor", "middle")
      .style("font-size", "15px")
      .style("font-family", "'Familjen Grotesk', sans-serif")
      .text("Cost (€/t of Glass)");

    svg.selectAll(".ylabel").data([0]).join("text")
      .attr("class", "ylabel")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", 20)
      .attr("text-anchor", "middle")
      .style("font-size", "15px")
      .style("font-family", "'Familjen Grotesk', sans-serif")
      .text("Emissions (t of CO₂/t of Glass)");

    const sortedData = [...data.filter(d => d.Case !== 'NG' && d.Case !== 'NG_CC'),
                        ...data.filter(d => d.Case === 'NG' || d.Case === 'NG_CC')];

    const points = svg.selectAll("path.point")
      .data(sortedData.filter(d => d[year] !== undefined && !isNaN(d[year]) && d.EI !== undefined), d => d.Case);

    points.enter()
      .append("path")
      .attr("class", "point")
      .attr("transform", d => `translate(${x(d[year])}, ${y(d.EI)})`)
      .attr("d", d => d3.symbol().type(d3.symbolCircle).size(200)())
      .attr("fill", d => /_CC/.test(d.Case) ? "none" : color(d.Spec_Energy))
      .attr("stroke", d => /_CC/.test(d.Case) ? color(d.Spec_Energy) : "black")
      .attr("stroke-width", 1.5)
      .on("mouseover", (event, d) => {
        tooltip.style("display", "block")
          .html(`<strong>${d.Case}</strong><br/>Cost: €${d[year].toFixed(2)}<br/>Emissions: ${d.EI}<br/>Spec Energy: ${d.Spec_Energy}`);
      })
      .on("mousemove", event => {
        tooltip.style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseout", () => {
        tooltip.style("display", "none");
      });

    points.transition().duration(1000)
      .attr("transform", d => `translate(${x(d[year])}, ${y(d.EI)})`)
      .attr("fill", d => /_CC/.test(d.Case) ? "none" : color(d.Spec_Energy))
      .attr("stroke", d => /_CC/.test(d.Case) ? color(d.Spec_Energy) : "black")
      .selection() // Get back to D3 selection
      .on("mouseover", (event, d) => {
        tooltip.style("display", "block")
          .html(`<strong>${d.Case}</strong><br/>TAC: €${d[year].toFixed(2)}<br/>Specific Emissions: ${d.EI}<br/>Specific Energy Consumption: ${d.Spec_Energy}`);
      })
      .on("mousemove", event => {
        tooltip.style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseout", () => {
        tooltip.style("display", "none");
    });
    
    const baseCase = data.find(d => d.Case === "base_case");
    const baseLine = svg.selectAll(".baseline").data(baseCase ? [baseCase] : []);

    baseLine.enter()
      .append("line")
      .attr("class", "baseline")
      .merge(baseLine)
      .transition().duration(1000)
      .attr("x1", d => x(d["2025"]))
      .attr("x2", d => x(d["2025"]))
      .attr("y1", margin.top)
      .attr("y2", height - margin.bottom)
      .attr("stroke", "gray")
      .attr("stroke-dasharray", "4")
      .attr("stroke-width", 1.5);

    const defs = svg.select("defs").empty() ? svg.append("defs") : svg.select("defs");
    const gradient = defs.select("#color-gradient").empty()
      ? defs.append("linearGradient").attr("id", "color-gradient").attr("x1", "0%").attr("y1", "100%").attr("x2", "0%").attr("y2", "0%")
      : defs.select("#color-gradient");

    gradient.selectAll("stop").data(d3.range(101)).join("stop")
      .attr("offset", d => `${d}%`)
      .attr("stop-color", d => d3.interpolateTurbo(d / 100));

    const legendX = width - margin.right + 40;
    const legendY = margin.top;
    const legendHeight = height - margin.top - margin.bottom;
    const legendWidth = 15;

    svg.selectAll("rect.colorbar").data([0]).join("rect")
      .attr("class", "colorbar")
      .attr("x", legendX)
      .attr("y", legendY)
      .attr("width", legendWidth)
      .attr("height", legendHeight)
      .style("fill", "url(#color-gradient)");

    // Get the min, mid, max of the energy domain
    const [minEnergy, maxEnergy] = d3.extent(data, d => d.Spec_Energy);
    const midEnergy = ((minEnergy + maxEnergy) / 2).toFixed(2);
    // Create a scale for colorbar ticks
    // const energyScale = d3.scaleLinear()
    //   .domain([minEnergy, maxEnergy])
    //   .range([legendY + legendHeight, legendY]);

    const ticks = [
      { value: minEnergy.toFixed(2), y: legendY + legendHeight },
      { value: midEnergy, y: legendY + legendHeight / 2 },
      { value: maxEnergy.toFixed(2), y: legendY }
    ];
    // Add colorbar tick labels
    svg.selectAll("text.energy-tick").data(ticks).join("text")
      .attr("class", "energy-tick")
      .attr("x", legendX + legendWidth + 5)
      .attr("y", d => d.y)
      .attr("text-anchor", "start")
      .attr("alignment-baseline", "middle")
      .style("font-size", "12px")
      .style("font-family", "'Familjen Grotesk', sans-serif")
      .text(d => d.value);

      svg.selectAll("text.colorbar-label").data([0]).join("text")
      .attr("class", "colorbar-label")
      .attr("transform", `translate(${legendX - 10}, ${legendY + legendHeight / 2}) rotate(-90)`)
      .attr("text-anchor", "middle")
      .style("font-size", "14px")
      .style("font-family", "'Familjen Grotesk', sans-serif")
      .text("Spec Energy (GJ/t)");    

    const legendGroup = svg.selectAll("g.legend-group").data([0]).join("g")
      .attr("class", "legend-group")
      .attr("transform", `translate(${(width - 145) / 2}, ${margin.top + 15})`);

    legendGroup.selectAll("circle.legend1").data([0]).join("circle")
      .attr("class", "legend1")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("r", 6)
      .style("fill", "#999")
      .style("stroke", "black");

    legendGroup.selectAll("text.legend1").data([0]).join("text")
      .attr("class", "legend1")
      .attr("x", 10)
      .attr("y", 1)
      .text("Without CC")
      .style("font-size", "15px")
      .style("font-family", "'Familjen Grotesk', sans-serif")
      .attr("alignment-baseline", "middle");

    legendGroup.selectAll("circle.legend2").data([0]).join("circle")
      .attr("class", "legend2")
      .attr("cx", 110)
      .attr("cy", 0)
      .attr("r", 6)
      .style("fill", "none")
      .style("stroke", "#999");

    legendGroup.selectAll("text.legend2").data([0]).join("text")
      .attr("class", "legend2")
      .attr("x", 120)
      .attr("y", 1)
      .text("With CC")
      .style("font-size", "15px")
      .style("font-family", "'Familjen Grotesk', sans-serif")
      .attr("alignment-baseline", "middle");

    svg.selectAll("foreignObject.selector").data([0]).join("foreignObject")
      .attr("class", "selector")
      .attr("x", width / 10 - 130)
      .attr("y", 25)
      .attr("width", 600)
      .attr("height", 60)
      .html(`
        <div xmlns="http://www.w3.org/1999/xhtml" style="
          text-align: center;
          margin: 0 auto;
          font-size: 16px;
          font-family: 'Familjen Grotesk', sans-serif;
          color: #222;
        ">
          <span style="font-weight: 600;">Please select the scenario year for the analysis:</span>
          <select style="
            font-size: 16px;
            padding: 5px 10px;
            border-radius: 6px;
            border: 1px solid #aaa;
            margin-left: 10px;
            font-family: 'Familjen Grotesk', sans-serif;
          ">
            <option value="2025" ${year === "2025" ? "selected" : ""}>2025</option>
            <option value="2030" ${year === "2030" ? "selected" : ""}>2030</option>
            <option value="2040" ${year === "2040" ? "selected" : ""}>2040</option>
            <option value="2050" ${year === "2050" ? "selected" : ""}>2050</option>
          </select>
        </div>
      `);

    svg.select("foreignObject.selector select").on("input", function () {
      setYear(this.value);
    });

  }, [year]);

  return <svg ref={svgRef} width={900} height={600}></svg>;
};

export default ParetoPlot;
